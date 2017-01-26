import os
import sys
import djclick as click

from .cli import fingerprint
from .cli import maintenance


@click.group()
def cli():
    """Library CLI"""
    pass


cli.add_command(fingerprint.cli)
#cli.add_command(maintenance.cli)
