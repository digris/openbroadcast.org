#-*- coding: utf-8 -*-

from datetime import datetime, timedelta
import djclick as click
from django.conf import settings

MEDIA_ASSET_KEEP_DAYS = getattr(settings, 'MEDIA_ASSET_KEEP_DAYS', 60)



@click.group()
def cli():
    """Platform CLI"""
    pass


@cli.command()
def check():
    click.secho('--------------------------------------------------------------------', bold=True)


@cli.command()
def delete_orphaned_tags():

    from tagging.models import TaggedItem
    to_delete = []
    tagged_items = TaggedItem.objects.all().nocache()

    with click.progressbar(tagged_items, label='Scanning {} tagged items'.format(tagged_items.count())) as bar:
        for ti in bar:
            if not ti.object:
                to_delete.append(ti.pk)

    click.echo('Total tagged items:    {}'.format(tagged_items.count()))
    click.echo('Orphaned tagged items: {}'.format(len(to_delete)))

    TaggedItem.objects.filter(pk__in=to_delete).delete()



@cli.command()
@click.option('--age', '-a', type=int, default=MEDIA_ASSET_KEEP_DAYS, help='Clean media assets not accessed for the last {0} days'.format(MEDIA_ASSET_KEEP_DAYS))
def clean_assets(age):

    from media_asset.models import Format
    from media_asset.models import Waveform

    format_qs = Format.objects.filter(
        accessed__lte=datetime.now() - timedelta(days=age)
    ).nocache()

    waveform_qs = Waveform.objects.filter(
        accessed__lte=datetime.now() - timedelta(days=age)
    ).nocache()


    with click.progressbar(format_qs, label='Deleting {} media format versions'.format(format_qs.count())) as bar:
        for item in bar:
            item.delete()

    with click.progressbar(waveform_qs, label='Deleting {} waveforms'.format(waveform_qs.count())) as bar:
        for item in bar:
            item.delete()


@cli.command()
def reset():
    # TODO: implement reset command
    raise NotImplementedError('reset command not implemented yet')


@cli.command()
def crawl():
    # TODO: implement crawl command
    raise NotImplementedError('crawl command not implemented yet')






#
# @cli.command()
# @click.option('--path', '-p', type=click.Path(), required=True)
# @click.option('--username', '-u', type=unicode, required=True)
# @click.option('--collection', '-c', type=unicode)
# @click.option('--limit', '-l', type=click.IntRange(1, 50000, clamp=True), default=100)
# def start(path, limit, username, collection):
#     """Start an import session"""
#
#     click.secho('--------------------------------------------------------------------', bold=True)
#     click.echo('Username:\t {}'.format(username))
#     click.echo('Collection:\t {}'.format(collection))
#     click.echo('Limit:\t\t {}'.format(limit))
#     click.echo('Path:\t\t {}'.format(path))
#     click.secho('--------------------------------------------------------------------', bold=True)
#     click.echo('')
#
#     if not os.path.isdir(path):
#         click.secho('Directory does not exist: {}'.format(path), bold=True, fg='red')
#         return
#
#     if not path.endswith('/'):
#         path += '/'
#
#     if not User.objects.filter(username=username).exists():
#         click.secho('User does not exist: {}'.format(username), bold=True, fg='red')
#         return
#
#     if Massimport.objects.filter(directory=path).exists():
#         click.secho('Import session already exists: {}'.format(path), bold=True, fg='red')
#         return
#
#
#     massimport = Massimport(
#         directory=path,
#         user=User.objects.get(username=username),
#         collection_name=collection
#     )
#
#     massimport.save()
#
#     if click.confirm('Continue with scanning directories?', default='Y'):
#         massimport.scan()
#
#     if click.confirm('Continue with enqueuing files?'):
#
#         for item in massimport.files.filter(status=0)[0:limit]:
#             item.enqueue()
#
