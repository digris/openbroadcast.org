#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys

import time
import tqdm
import djclick as click
from optparse import make_option
from django.contrib.auth.models import User
from django.conf import settings
from django.core.management.base import BaseCommand, NoArgsCommand

from massimporter.models import Massimport, MassimportFile

DEFAULT_LIMIT = 100
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)


"""
massimporter cli

default usage:

    ./manage.py massimporter_cli start /path/to/import
    # returns the id
    ./manage.py massimporter_cli enqueue <id>


"""



@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass
    #click.echo(click.style('Debug mode is %s' % ('on' if debug else 'off'), bold=True))



@cli.command()
@click.argument('id', type=int, required=False)
def status(id):

    if not id:

        massimports = Massimport.objects.order_by('status').all()

        tpl = '''{id}\t{status}\t{num_files}\t{username}\t{directory}'''

        click.secho('--------------------------------------------------------------------', bold=True)
        click.secho('ID\tstatus\tfiles\tuser\tdirectory\t', bold=True)
        click.secho('--------------------------------------------------------------------', bold=True)

        for item in massimports:
            click.echo(tpl.format(
                id=item.pk,
                status=item.get_status_display(),
                username=item.user,
                num_files=item.files.count(),
                directory=item.directory,
            ))

        click.echo('')


    else:

        try:
            massimport = Massimport.objects.get(pk=id)
        except Massimport.DoesNotExist as e:
            click.secho('Massimport session with id: {} does not exist.'.format(id), bold=True, fg='red')
            return


        massimport.update()

        tpl = '''{}:    \t{}'''

        click.secho('--------------------------------------------------------------------', bold=True)
        click.secho('Status ({})\tcount'.format(id), bold=True)
        click.secho('--------------------------------------------------------------------', bold=True)

        for status in MassimportFile.STATUS_CHOICES:
            count = massimport.files.filter(status=status[0]).count()
            if count:
                click.echo(tpl.format(
                    status[1],
                    count
                ))

        click.secho('--------------------------------------------------------------------', bold=True)
        click.secho(('Total:    \t{}'.format(massimport.files.all().count())), bold=True)
        click.echo('')



@cli.command()
@click.argument('id', type=int)
def delete(id):

    try:
        massimport = Massimport.objects.get(pk=id)
    except Massimport.DoesNotExist as e:
        click.secho('Massimport session with id: {} does not exist.'.format(id), bold=True, fg='red')
        return

    if click.confirm('Do you want to delete session id: {} ?'.format(id), default='Y'):
        massimport.delete()



@cli.command()
@click.argument('id', type=int)
def scan(id):

    try:
        massimport = Massimport.objects.get(pk=id)
    except Massimport.DoesNotExist as e:
        click.secho('Massimport session with id: {} does not exist.'.format(id), bold=True, fg='red')
        return

    massimport.scan()


@cli.command()
@click.argument('id', type=int)
def update(id):

    try:
        massimport = Massimport.objects.get(pk=id)
    except Massimport.DoesNotExist as e:
        click.secho('Massimport session with id: {} does not exist.'.format(id), bold=True, fg='red')
        return

    massimport.update()


@cli.command()
@click.argument('id', type=int)
@click.option('--limit', '-l', type=click.IntRange(1, 50000, clamp=True), default=100)
def enqueue(id, limit):

    try:
        massimport = Massimport.objects.get(pk=id)
    except Massimport.DoesNotExist as e:
        click.secho('Massimport session with id: {} does not exist.'.format(id), bold=True, fg='red')
        return

    qs = massimport.files.filter(status=0)
    click.secho('Files total: {} - limit: {}'.format(qs.count(), limit), bold=True)
    for item in massimport.files.filter(status=0)[0:limit]:
        item.enqueue()



@cli.command()
@click.option('--path', '-p', type=click.Path(), required=True)
@click.option('--username', '-u', type=unicode, required=True)
@click.option('--collection', '-c', type=unicode)
@click.option('--limit', '-l', type=click.IntRange(1, 50000, clamp=True), default=100)
def start(path, limit, username, collection):

    click.secho('--------------------------------------------------------------------', bold=True)
    click.echo('Username:\t {}'.format(username))
    click.echo('Collection:\t {}'.format(collection))
    click.echo('Limit:\t\t {}'.format(limit))
    click.echo('Path:\t\t {}'.format(path))
    click.secho('--------------------------------------------------------------------', bold=True)
    click.echo('')

    if not os.path.isdir(path):
        click.secho('Directory does not exist: {}'.format(path), bold=True, fg='red')
        return

    if not path.endswith('/'):
        path += '/'

    if not User.objects.filter(username=username).exists():
        click.secho('User does not exist: {}'.format(username), bold=True, fg='red')
        return

    # if Massimport.objects.filter(directory=path).exists():
    #     click.secho('Import session already exists: {}'.format(path), bold=True, fg='red')
    #     return


    massimport = Massimport(
        directory=path,
        user=User.objects.get(username=username),
        collection_name=collection
    )

    massimport.save()

    if click.confirm('Continue with scanning directories?', default='Y'):
        massimport.scan()

    if click.confirm('Continue with enqueuing files?'):

        for item in massimport.files.filter(status=0)[0:limit]:
            item.enqueue()

