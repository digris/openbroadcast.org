#-*- coding: utf-8 -*-
from optparse import make_option
import os
import sys
import subprocess
import struct

from django.core.files import File as DjangoFile
from django.core.management.base import BaseCommand, NoArgsCommand
from django.template.defaultfilters import slugify
import audiotools

from alibrary.models import Artist, Release, Media, Label
from filer.models.filemodels import File
from filer.models.audiomodels import Audio
from filer.models.imagemodels import Image
from ep.API import fp
import echoprint


class FolderImporter(object):
    
    def __init__(self, * args, **kwargs):
        self.path = kwargs.get('path')
        self.label = kwargs.get('label')
        self.artist = kwargs.get('artist')
        self.release = kwargs.get('release')
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
        
        
        if not self.path:
            print
            print "Please specify a --path"
            print
            sys.exit(1)
        
        
        label_lookup = self.label
        artist_lookup = self.artist
        release_lookup = self.release
        
        force_label = None
        force_artist = None
        force_release = None
        
        if label_lookup:
            try:
                label_id = int(label_lookup)
            except ValueError, e:
                label_id = None
    
            if label_id:
                try:
                    force_label = Label.objects.get(pk=label_id)
                except Exception:
                    print 'Sorry - Could not find a Label with the given ID of %s' % label_id
                    sys.exit()
            else:
                try:
                    force_label, created = Label.objects.get_or_create(name=label_lookup)
                    if created:
                        print "Created label %s | id: %s" % (force_label.name, force_label.pk)
                except Exception:
                    print 'Sorry - Creation of label did not work out.'
                    print e
                    sys.exit()
        
        if artist_lookup:
            try:
                artist_id = int(artist_lookup)
            except ValueError, e:
                artist_id = None
    
            if artist_id:
                try:
                    force_artist = Artist.objects.get(pk=artist_id)
                except Exception:
                    print 'Sorry - Could not find a artist with the given ID of %s' % artist_id
                    sys.exit()
            else:
                try:
                    force_artist, created = Artist.objects.get_or_create(name=artist_lookup)
                    if created:
                        print "Created artist %s | id: %s" % (force_artist.name, force_artist.pk)
                except Exception:
                    print 'Sorry - Creation of artist did not work out.'
                    print e
                    sys.exit()
                

        
        if release_lookup:
            try:
                release_id = int(release_lookup)
            except ValueError, e:
                release_id = None
    
            if release_id:
                try:
                    force_release = Release.objects.get(pk=release_id)
                except Exception:
                    print 'Sorry - Could not find a release with the given ID of %s' % release_id
                    sys.exit()
            else:
                try:
                    force_release, created = Release.objects.get_or_create(name=release_lookup)
                    if created:
                        print "Created release %s | id: %s" % (force_release.name, force_release.pk)
                except Exception:
                    print 'Sorry - Creation of release did not work out.'
                    print e
                    sys.exit()


        print "#########################################################"
        print "Forced settings for:"
        print "#########################################################"
        print "Label:   %s" % force_label
        print "Artist:  %s" % force_artist
        print "Release: %s" % force_release
        print "#########################################################"
        print
        print
        print
     
        #sys.exit() 
        
        path = path or self.path
        path = unicode(os.path.normpath(path))

        file_list = []
        file_size = 0
        folder_count = 0
        rootdir = sys.argv[1]
        
        releases = []
        artists = []
        tracks = []
        
        for root, subFolders, files in os.walk(path):
            folder_count += len(subFolders)
            for file in files:
                f = os.path.join(root,file)
                file_size = file_size + os.path.getsize(f)
                rel_path = f[len(path):]                
                rel_path = rel_path.encode('ascii', 'ignore')


                if force_label:
                    label = force_label
                else:
                    label = None 
                    
                if force_artist:
                    artist = force_artist
                else:
                    artist = None 
                    
                if force_release:
                    release = force_release
                else:
                    release = None    
                
                
                try:
                    
                    full_path = os.path.join(root, file)
                    
                    audiofile = audiotools.open(full_path)
                    metadata = audiofile.get_metadata()

                    
                    if metadata:
                        artist_name = metadata.artist_name.strip()
                        release_name = metadata.album_name.strip()
                        track_name = metadata.track_name.strip()
                        tracknumber = metadata.track_number
                    else:
                        artist_name = 'Unknown'
                        release_name = 'Unknown'
                        track_name = file
                        tracknumber = 0
                    
                    print
                    print "*********************************************************"
                    print 'Extracted Metadata:'
                    print "*********************************************************"
                    print 'artist: %s' % artist_name
                    print 'release: %s' % release_name
                    print 'track: %s' % track_name
                    print 'tracknumber: %s' % tracknumber
                    print
                    
                    
                    # label - not in metadata...
                    
                    # artist
                    if not artist and artist_name:
                        artist, artist_created = Artist.objects.get_or_create(name=artist_name, slug=slugify(artist_name))
                        if artist_created:
                            print "Created artist '%s' | id: %s" % (artist.name, artist.pk)
                        else:
                            print "Existing artist '%s' | id: %s" % (artist.name, artist.pk)

                    # release
                    if not release and release_name:
                        release, release_created = Release.objects.get_or_create(name=release_name, slug=slugify(release_name))
                        if release_created:
                            print "Created release '%s' | id: %s" % (release.name, release.pk)
                        else:
                            print "Existing release '%s' | id: %s" % (release.name, release.pk)


                    skip_media = False
                    sample_duration = 30
                    print "************************************************"
                    print "Sample duration: %s" % audiofile.seconds_length()
                    if audiofile.seconds_length() < 40:
                        sample_duration = int(audiofile.seconds_length()) -10
                        
                    if audiofile.seconds_length() > 20:
                        
                        p = subprocess.Popen([
                            'ffmpeg', '-loglevel', 'quiet', '-i', full_path, '-ac', '1', '-ar', '11025', '-f', 's16le', '-t', '%s' % sample_duration, '-ss', '10', '-',
                        ], stdout=subprocess.PIPE)
                        
                        samples = []
                        while True:
                            sample = p.stdout.read(2)
                            if sample == '':
                                break
                            samples.append(struct.unpack('h', sample)[0] / 32768.0)
                        
                        d = echoprint.codegen(samples)                    
                        res = fp.best_match_for_query(d['code'])
                        
                        
                        
                        if res.match():
                            print 'Track already in database'
                            skip_media = True
                        else:
                            print 'New track, continue with import'
                    
                    
                    if not skip_media:

                        
                        media, media_created = Media.objects.get_or_create(name=track_name, tracknumber=tracknumber, artist=artist, release=release)
                    
                        print "MEDIA PK: %s" % media.pk
                    
                        dj_file = DjangoFile(open(os.path.join(root, file)), name=file)
                        print dj_file
                        
                        media.master = dj_file
                        media.save()
                        
                        
                            
                        if release and label:
                            release.label = label
                            release.save()
                            
                        if not release.main_image:
                            print 'Image missing'
                            tfile = 'temp/cover.jpg'
                            
                            audiofile = audiotools.open(os.path.join(root, file))
                            metadata = audiofile.get_metadata()
                            if metadata:
                                for image in metadata.images():
                                    #print image.data
                                    
                                    f = open(tfile,"wb")
                                    f.write(image.data)
                                    f.close()
                                    
                                    dj_file = DjangoFile(open(tfile), name='cover.jpg')
                                    
                                    cover = self.import_file(file=dj_file, folder=release.get_folder('pictures'))
                                    
                                    release.main_image = cover
        
                                    release.save()

                            
                        
                    
                except Exception, e:
                    print e
                    pass
                
        




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
        make_option('--label',
            action='store',
            dest='label',
            default=False,
            help='Force label (Name or id)'),
        make_option('--artist',
            action='store',
            dest='artist',
            default=False,
            help='Force artist (Name or id)'),
        make_option('--release',
            action='store',
            dest='release',
            default=False,
            help='Force release (Name or id)'),
        )

    def handle_noargs(self, **options):
        folder_importer = FolderImporter(**options)
        folder_importer.walker()
