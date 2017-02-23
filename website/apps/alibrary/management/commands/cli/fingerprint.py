import djclick as click


@click.group()
def cli():
    """Accoustic Fingerprint CLI"""
    pass


@cli.command()
def delete():
    """Deletes all fingerprints"""
    from ep.API import fp
    from alibrary.models import Media

    if click.confirm('Are you sure to delete all acoustic fingerprints?'):
        fp.erase_database(True)
        Media.objects.all().update(echoprint_status=0)

        click.echo('All acoustic fingerprints deleted.')


@cli.command()
def create():
    """Recreate all fingerprints"""
    from alibrary.models import Media

    qs = Media.objects.exclude(master='')
    with click.progressbar(qs, label='Updating fingerprints', length=qs.count()) as items:
        for item in items:
            try:
                item.update_echoprint()
            except OSError as e:
                click.echo(e)
                pass


@cli.command()
def status():
    """Show fingerprint statistics"""
    from alibrary.models import Media

    qs = Media.objects.all()

    click.secho('--------------------------------------------------------------------', bold=True)
    click.secho('Total:     {}'.format(qs.count()), bold=True)
    click.secho('Init:      {}'.format(qs.filter(echoprint_status=0).count()), fg='cyan')
    click.secho('Assigned:  {}'.format(qs.filter(echoprint_status=1).count()), fg='green')
    click.secho('Skipped:   {}'.format(qs.filter(echoprint_status=3).count()), fg='yellow')
    click.secho('Error:     {}'.format(qs.filter(echoprint_status__in=[2, 99]).count()), fg='red')
    click.secho('--------------------------------------------------------------------', bold=True)
    click.echo('')
