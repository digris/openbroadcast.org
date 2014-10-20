#-*- coding: utf-8 -*-
from optparse import make_option
import os
import sys
import re

from django.core.files import File as DjangoFile
from django.core.management.base import BaseCommand, NoArgsCommand
from django.template.defaultfilters import slugify
import audiotools

from alibrary.models import Artist, Release, Media, Label
from filer.models.filemodels import File
from filer.models.audiomodels import Audio
from filer.models.imagemodels import Image


class FolderImporter(object):
    def __init__(self, * args, **kwargs):
        self.path = kwargs.get('path')
        self.verbosity = int(kwargs.get('verbosity', 1))


    def import_file(self, file, folder):
        
        print "#########################"
        print folder.name
        print "#########################"
        

        """
        Create a Audio or an Image into the given folder
        """
        try:
            iext = os.path.splitext(file.name)[1].lower()
        except:
            iext = ''
            
        print 'iext:'
        print iext 
            
        if iext in ['.jpg', '.jpeg', '.png', '.gif']:
            obj, created = Image.objects.get_or_create(
                                original_filename=file.name,
                                file=file,
                                folder=folder,
                                is_public=True)
            
            print 'obj:',
            print obj
            
            
            
        if iext in ['.mp3', '.flac', '.wav', '.aiff']:
            obj, created = Audio.objects.get_or_create(
                                original_filename=file.name,
                                file=file,
                                folder=folder,
                                is_public=False)

        if obj:
            print 'have object'
            return obj
        else:
            return None



    def walker(self, path=None, base_folder=None):
        
        
        # Hardcoded as it is a test only...
        
        label_name = 'HH-Digital'
        label = Label.objects.get(name=label_name)
        
        
        path = path or self.path
        path = unicode(os.path.normpath(path))


        file_list = []
        file_size = 0
        folder_count = 0
        rootdir = sys.argv[1]
        
        releases = []
        artists = []
        tracks = []
        
        
        #pattern = "^/[A-Za-z0-9.]/*$"

        pattern = re.compile('^/(?P<artist>[a-zA-Z0-9 ]+)/(?P<release>[a-zA-Z0-9 ]+)/(?P<tracknumber>[\d]+)[ ]* - [ ]*(?P<track>[a-zA-Z0-9 -_]+)\.[a-zA-Z]+.*')
        
        pattern = re.compile('^/(?P<artist>[a-zA-Z0-9 ]+)/(?P<release>[a-zA-Z0-9 ]+)/(?P<tracknumber>[ab]?\d+?)[ | - ](?P<track>[Ça-zA-Z0-9 -_]+)\.[a-zA-Z]+.*')
        
        '^/(?P<release>[a-zA-Z0-9 ]+)/(?P<tracknumber>[ab]?\d+?)[ | -](?P<artist>[a-zA-Z0-9 ]+) - (?P<track>[Ça-zA-Z0-9 -_]+)\.[a-zA-Z]+.*'

        for root, subFolders, files in os.walk(path):
            folder_count += len(subFolders)
            for file in files:
                f = os.path.join(root,file)
                file_size = file_size + os.path.getsize(f)
                
                rel_path = f[len(path):]
                
                rel_path = rel_path.encode('ascii', 'ignore')


                #rel_path = '/The Prodigy/The Fat Of The Land/04 - Funky Stuff.flac'
                
                match = pattern.search(rel_path)
                
                #print
                #print
                print '-------------------------------------------------------------'
                
                try:
                    
                    print match.groups()
                    
                    artist_name = match.group('artist')
                    release_name = match.group('release')
                    track_name = match.group('track')
                    tracknumber = match.group('tracknumber')
                    """
                    print 'artist: %s' % artist_name
                    print 'release: %s' % release_name
                    print 'track: %s' % track_name
                    print 'tracknumber: %s' % tracknumber
                    """
                    
                    
                    if not artist_name in artists:
                        artists.append(artist_name)
                        
                    if not release_name in releases:
                        releases.append(release_name)
                    
                    
                    """"""
                    release, release_created = Release.objects.get_or_create(name=release_name, slug=slugify(release_name), label=label)
                    artist, artist_created = Artist.objects.get_or_create(name=artist_name, slug=slugify(artist_name))
                    media, media_created = Media.objects.get_or_create(name=track_name, tracknumber=tracknumber, artist=artist, release=release)
                    
                    dj_file = DjangoFile(open(os.path.join(root, file)), name=file)
                    
                    """
                    print "**:", 
                    print dj_file,
                    print dj_file.size
                    """
                    
                    if not media.master:
                        master = self.import_file(file=dj_file, folder=release.get_folder('tracks'))
                        media.master = master
                        media.save()
                        
                        
                        
                    if not release.main_image:
                        print 'Image missing'
                        
                        tfile = 'temp/cover.jpg'
                        
                        audiofile = audiotools.open(os.path.join(root, file))
                        
                        metadata = audiofile.get_metadata()
                        for image in metadata.images():
                            #print image.data
                            
                            f = open(tfile,"wb")
                            f.write(image.data)
                            f.close()
                            
                            dj_file = DjangoFile(open(tfile), name='cover.jpg')
                            
                            cover = self.import_file(file=dj_file, folder=release.get_folder('pictures'))
                            
                            release.main_image = cover

                            release.save()
                            
                        
                        #track.get_metadata()
                        
                        pass
                        
                        
                        
                    
                    """                        
                    artist, artist_created = Artist.objects.get_or_create(name=artist_name)
                    if not artist_created:
                        #pass
                        artist.save()
                    """ 
                    
                except Exception, e:
                    print e
                    pass
                
                # help(match)
                
                #print match.group(0)
                
                # print match
                
                
                 
                #print(f)
                #print rel_path
                file_list.append(f)
        
        #print("Total Size is {0} bytes".format(file_size))
        #print("Total Files ", len(file_list))
        #print("Total Folders ", folder_count)


        
        print "# Artists ----------------------------------------------"
        print artists
        
        print "# Releases ---------------------------------------------"
        print releases


        """
        for root, dirs, files in os.walk(path):
            print files
            for file in files:
                print file
        """



class Command(NoArgsCommand):
    """
    Import directory structure into alibrary:

        manage.py import_folder --path=/tmp/assets/images
    """

    option_list = BaseCommand.option_list + (
        make_option('--path',
            action='store',
            dest='path',
            default=False,
            help='Import files located in the path into django-filer'),
        )

    def handle_noargs(self, **options):
        folder_importer = FolderImporter(**options)
        folder_importer.walker()
