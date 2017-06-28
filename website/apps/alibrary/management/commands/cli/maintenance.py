import djclick as click
from alibrary.models import Media


@click.group()
def cli():
    """Maintenance CLI"""
    pass


@cli.command()
def repair_durations():

    """Repair/reprocess master durations."""

    from base.audio.fileinfo import FileInfoProcessor

    tolerance = 0.1

    items_to_reprocess = []

    qs = Media.objects.exclude(master='').order_by('pk')

    with click.progressbar(qs, label='Reprocessing {} tracks'.format(qs.count())) as bar:
        for item in bar:

            p = FileInfoProcessor(item.master.path)

            current_duration = item.master_duration
            new_duration = p.duration

            diff = current_duration - new_duration

            if diff > tolerance:
                items_to_reprocess.append(item)

            # print(item.master_duration)

    click.echo('{} tracks have differences in duration'.format(len(items_to_reprocess)))





