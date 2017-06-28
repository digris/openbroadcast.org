import djclick as click
from django.db import close_old_connections
from alibrary.models import Media


@click.group()
def cli():
    """Maintenance CLI"""
    pass


@cli.command()
@click.option('--dump-to', type=click.File('wb'))
@click.option('--load-from', type=click.File('rb'))
@click.option('--tolerance', type=float, default=0.5)
@click.option('--log-file', type=click.File('wb'))
def repair_durations(dump_to, load_from, tolerance, log_file):

    """Repair/reprocess master durations."""

    from base.audio.fileinfo import FileInfoProcessor

    items_to_reprocess = []
    affected_playlists = []




    if load_from:

        click.echo('loading ids from dump file')
        item_ids = [
            int(l.strip().split(',')[0]) for l in load_from.readlines()
        ]

        items_to_reprocess = Media.objects.filter(pk__in=item_ids)

    else:

        # mysql does not support remote/streaming cursors
        # to save memory items are loaded from db individually

        values = Media.objects.order_by('pk').values('id')
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

        tpl = u'''id: {id} - "{name}"
{url}
        '''


        tpl_log = u'{ct},{pk},{url},{type}\n'

        # write column header
        if log_file:
            log_file.write(tpl_log.format(
                ct='content-type',
                pk='id',
                url='url',
                type='type',
            ))


        for item in items_to_reprocess:
            click.echo(tpl.format(
                id=item.id,
                name=item.name,
                url=item.get_absolute_url(),
            ))

            if log_file:
                log_file.write(tpl_log.format(
                    ct='media',
                    pk=item.pk,
                    url=item.get_absolute_url(),
                    type=item.get_mediatype_display(),
                ))
                log_file.flush()

            for p in item.get_appearances():
                if not p in affected_playlists:
                    affected_playlists.append(p)


        for item in affected_playlists:
            click.echo(tpl.format(
                id=item.id,
                name=item.name,
                url=item.get_absolute_url(),
            ))

            if log_file:
                log_file.write(tpl_log.format(
                    ct='playlist',
                    pk=item.pk,
                    url=item.get_absolute_url(),
                    type=item.get_type_display(),
                ))
                log_file.flush()







