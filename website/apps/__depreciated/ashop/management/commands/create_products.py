#-*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand, NoArgsCommand

from alibrary.models import Release, Media, Format
from ashop.models import Downloadrelease, Downloadmedia


class ProductCreator(object):
    def __init__(self, * args, **kwargs):
        self.type = kwargs.get('type')
        self.price = int(kwargs.get('price'))

    def create(self, path=None, base_folder=None):
        print self.type
        
        formats = Format.objects.all()
        
        if self.type == 'release':
            releases = Release.objects.filter(releaseproduct=None)
            for release in releases:
                
                for format in formats:
                    price = format.default_price
                    if self.price:
                        price = self.price
                    
                    product, created = Downloadrelease.objects.get_or_create(release=release, format=format, unit_price=price, active=True)
                    product.release = release
                    product.save()
                
                print release
        
        if self.type == 'media' or self.type == 'track': # unify
            # yes i know that "medias" is not the correct plural... 
            medias = Media.objects.filter(mediaproduct=None)
            for media in medias:
                
                for format in formats:
                    price = format.default_price
                    if self.price:
                        price = self.price
                    
                    """"""
                    product, created = Downloadmedia.objects.get_or_create(media=media, format=format, unit_price=price, active=True)
                    product.media = media
                    product.save()
                    
                    
                print media

                
        




class Command(NoArgsCommand):
    """
    Import directory structure into alibrary:

        manage.py import_folder --path=/tmp/assets/images
    """

    option_list = BaseCommand.option_list + (
        make_option('--type',
            action='store',
            dest='type',
            default=False,
            help='Create downloadable products'),
        make_option('--price',
            action='store',
            dest='price',
            default=False,
            help='Default price'),
        )

    def handle_noargs(self, **options):
        product_creator = ProductCreator(**options)
        product_creator.create()
