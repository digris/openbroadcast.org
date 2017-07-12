import djclick as click
from django.db import close_old_connections
from django.contrib.sites.models import Site
from cacheops import invalidate_obj, invalidate_model
from alibrary.models import Media, Playlist




@click.group()
def cli():
    """Maintenance CLI"""
    pass


@cli.command()
@click.option('--limit-range', type=str, help='limit range/offset. e.g. "170:190"')
@click.option('--dump-to', type=click.File('ab'))
@click.option('--load-from', type=click.File('rb'))
@click.option('--tolerance', type=float, default=0.5)
@click.option('--log-file', type=click.File('wb'))
def repair_durations(limit_range, dump_to, load_from, tolerance, log_file):
    """
    Repair/reprocess master durations.
    """
    from base.audio.fileinfo import FileInfoProcessor

    items_to_reprocess = []
    affected_playlists = []
    affected_playlist_ids = []

    # invalidate cache for Media
    invalidate_model(Media)

    if load_from:

        if limit_range:
            raise NotImplementedError('--limit-range option not allowed in combination with --load-from')

        # using `set` to remove duplicate ids
        item_ids = set([
            int(l.strip().split(',')[0]) for l in load_from.readlines() if float(l.strip().split(',')[1]) > tolerance
        ])


        click.echo('loaded {} ids from dump file'.format(len(item_ids)))

        items_to_reprocess = Media.objects.filter(pk__in=item_ids)

    else:

        # mysql does not support remote/streaming cursors
        # to save memory items are loaded from db individually
        values = Media.objects.order_by('pk').values('id').nocache()

        if limit_range:
            _limits = limit_range.split(':')
            values = values[_limits[0]:_limits[1]]

        item_ids = [i['id'] for i in values]

        with click.progressbar(item_ids, show_pos=True, width=48, label='Reprocessing {} tracks'.format(len(item_ids))) as bar:

            for item_pk in bar:

                close_old_connections()

                item = Media.objects.get(pk=item_pk)

                if item.master and item.master.path:

                    p = FileInfoProcessor(item.master.path)

                    current_duration = item.master_duration
                    new_duration = p.duration

                    try:
                        diff = abs(current_duration - new_duration)
                    except TypeError:
                        diff = 100.0

                    if diff > tolerance:
                        items_to_reprocess.append(item)

                    # add to csv log
                    if diff > tolerance and dump_to:
                        dump_to.write('{pk},{diff}\n'.format(pk=item.pk, diff=diff))
                        dump_to.flush()


    click.echo('{} tracks have differences in duration'.format(len(items_to_reprocess)))


    if click.confirm('Do you want to update/repair the durations on {} tracks?'.format(len(items_to_reprocess))):

        base_url = 'http://{}'.format(Site.objects.get_current().domain)


        tpl = u'''id: {id} - "{name}"
{url}
old: {current_duration} new: {new_duration} diff: {diff}
        '''


        tpl_log = u'{ct},{pk},{type},{current_duration},{new_duration},{diff},{url}\n'

        # write column header
        if log_file:
            log_file.write(tpl_log.format(
                ct='content-type',
                pk='id',
                url='url',
                type='type',
                #
                current_duration='old_duration',
                new_duration='new_duration',
                diff='diff',
            ))


        # loop affected media, fix durations, get playlist appearances & print/log info
        for item in items_to_reprocess:

            p = FileInfoProcessor(item.master.path)

            current_duration = item.master_duration
            new_duration = p.duration

            try:
                diff = current_duration - new_duration
            except TypeError:
                diff = '-'


            click.echo(tpl.format(
                id=item.id,
                name=item.name,
                url=base_url + item.get_absolute_url(),
                #
                current_duration=current_duration,
                new_duration=new_duration,
                diff=diff
            ))

            if log_file:
                log_file.write(tpl_log.format(
                    ct='media',
                    pk=item.pk,
                    url=base_url + item.get_absolute_url(),
                    type=item.get_mediatype_display(),
                    #
                    current_duration=current_duration,
                    new_duration=new_duration,
                    diff=diff
                ))
                log_file.flush()

            for p in item.get_appearances():
                if not p.pk in affected_playlist_ids:
                    affected_playlist_ids.append(p.pk)
                    # we need to store the 'current' value of the duration
                    affected_playlists.append({
                        'obj': p,
                        'current_duration': p.get_duration()
                    })

            # update media duration
            Media.objects.filter(pk=item.pk).update(master_duration=new_duration)
            invalidate_obj(item)


        # loop playlists & print/log info
        for item in affected_playlists:

            invalidate_obj(item['obj'])

            current_duration = float(item['current_duration']) / 1000
            new_duration = float(item['obj'].get_duration()) / 1000

            try:
                diff = current_duration - new_duration
            except TypeError:
                diff = '-'

            click.echo(tpl.format(
                id=item['obj'].id,
                name=item['obj'].name,
                url=base_url + item['obj'].get_absolute_url(),
                #
                current_duration=current_duration,
                new_duration=new_duration,
                diff=diff
            ))

            if log_file:
                log_file.write(tpl_log.format(
                    ct='playlist',
                    pk=item['obj'].pk,
                    url=base_url + item['obj'].get_absolute_url(),
                    type=item['obj'].get_type_display(),
                    #
                    current_duration=current_duration,
                    new_duration=new_duration,
                    diff=diff
                ))
                log_file.flush()

            # update playlist duration
            Playlist.objects.filter(pk=item['obj'].pk).update(duration=new_duration * 1000)
            invalidate_obj(item)



@cli.command()
def generate_master_hashes():
    """
    Generate missing sha1 hashes
    """

    # mysql does not support remote/streaming cursors
    # to save memory items are loaded from db individually
    values = Media.objects.filter(master_sha1__isnull=True).order_by('pk').values('id').nocache()

    item_ids = [i['id'] for i in values]

    with click.progressbar(item_ids, show_pos=True, width=48,label='Reprocessing {} hashes'.format(len(item_ids))) as bar:

        for item_pk in bar:

            close_old_connections()

            item = Media.objects.get(pk=item_pk)

            if item.master and item.master.path:

                master_sha1 = item.generate_sha1()

                # update media duration
                Media.objects.filter(pk=item.pk).update(master_sha1=master_sha1)
