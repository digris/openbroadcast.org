import djclick as click


@click.group()
def cli():
    """Maintenance CLI"""
    pass


@cli.command()
def version():
    """Display the current version."""
    click.echo('mntncns bla the bli')