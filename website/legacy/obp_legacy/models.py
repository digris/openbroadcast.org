# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Artists(models.Model):
    id = models.IntegerField(primary_key=True)
    tagquality = models.IntegerField()
    name = models.CharField(max_length=750, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=60, blank=True)
    artist_type = models.CharField(max_length=60, blank=True)
    editable = models.IntegerField()
    owner = models.CharField(max_length=750, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    edits = models.IntegerField()
    profile = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    artisttype = models.CharField(max_length=300, blank=True)
    contact = models.CharField(max_length=750, blank=True)
    booking = models.CharField(max_length=750, blank=True)
    realname = models.CharField(max_length=750, blank=True)
    country = models.CharField(max_length=6, blank=True)
    aliases = models.CharField(max_length=750, blank=True)
    pipeline_status = models.IntegerField()
    mb_artistid = models.CharField(max_length=108, blank=True)
    discogs_artistid = models.CharField(max_length=750, blank=True)
    discogs_status = models.IntegerField()
    mb_status = models.IntegerField()
    lastfm_url = models.CharField(max_length=750, blank=True)
    lastfm_status = models.IntegerField()
    wikipedia_url = models.CharField(max_length=750, blank=True)
    myspace_url = models.CharField(max_length=750, blank=True)
    soundcloud_url = models.CharField(max_length=1500, blank=True)
    facebook_url = models.CharField(max_length=1500, blank=True)
    various_links = models.TextField(blank=True)
    tags = models.CharField(max_length=750, blank=True)
    website = models.CharField(max_length=750, blank=True)
    has_image = models.IntegerField(null=True, blank=True)
    lock = models.IntegerField()
    autopublish = models.IntegerField()
    migrated = models.DateTimeField(null=True, blank=True)
    total_downloads = models.IntegerField()
    total_plays = models.IntegerField()
    class Meta:
        db_table = u'artists'

class Labels(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=750, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=60, blank=True)
    editable = models.IntegerField()
    label_type = models.CharField(max_length=150, blank=True)
    label_code = models.CharField(max_length=750, blank=True)
    owner = models.CharField(max_length=750, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    edits = models.IntegerField()
    profile = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    contact = models.CharField(max_length=750, blank=True)
    address = models.CharField(max_length=750, blank=True)
    country = models.CharField(max_length=150, blank=True)
    distributor = models.CharField(max_length=750, blank=True)
    distributor_contact = models.CharField(max_length=750, blank=True)
    license_type = models.CharField(max_length=300, blank=True)
    license_source = models.CharField(max_length=300, blank=True)
    license_provider = models.CharField(max_length=300, blank=True)
    license_rights = models.CharField(max_length=750, blank=True)
    license_conditions = models.CharField(max_length=750, blank=True)
    license_notes = models.TextField(blank=True)
    pipeline_status = models.IntegerField()
    mb_labelid = models.CharField(max_length=108, blank=True)
    mb_status = models.IntegerField()
    discogs_labelid = models.CharField(max_length=750, blank=True)
    discogs_status = models.IntegerField()
    lastfm_url = models.CharField(max_length=750, blank=True)
    lastfm_status = models.IntegerField()
    wikipedia_url = models.CharField(max_length=750, blank=True)
    
    facebook_url = models.CharField(max_length=750, blank=True)
    soundcloud_url = models.CharField(max_length=750, blank=True)
    
    various_links = models.TextField(blank=True)
    website = models.CharField(max_length=750, blank=True)
    parent_labelid = models.IntegerField(null=True, blank=True)
    has_image = models.IntegerField(null=True, blank=True)
    lock = models.IntegerField()
    autopublish = models.IntegerField()
    migrated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'labels'

class Licenses(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    key = models.CharField(max_length=150, blank=True)
    version = models.IntegerField()
    restricted = models.IntegerField()
    lock = models.IntegerField()
    class Meta:
        db_table = u'licenses'

class Medias(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=60, blank=True)
    editable = models.IntegerField()
    owner = models.CharField(max_length=256)
    user_id = models.IntegerField(null=True, blank=True)
    edits = models.IntegerField()
    notes = models.TextField(blank=True)
    filesize = models.IntegerField(null=True, blank=True)
    fileformat = models.CharField(max_length=36, blank=True)
    dataformat = models.CharField(max_length=36, blank=True)
    channels = models.IntegerField(null=True, blank=True)
    sample_rate = models.IntegerField(null=True, blank=True)
    bitrate = models.IntegerField(null=True, blank=True)
    channelmode = models.CharField(max_length=36, blank=True)
    bitrate_mode = models.CharField(max_length=36, blank=True)
    lossless = models.IntegerField(null=True, blank=True)
    encoder_options = models.CharField(max_length=36, blank=True)
    compression_ratio = models.DecimalField(null=True, max_digits=14, decimal_places=4, blank=True)
    encoding = models.CharField(max_length=36, blank=True)
    path = models.CharField(max_length=512, blank=True)
    parentdirectory = models.CharField(max_length=512, blank=True)
    filename = models.CharField(max_length=512, blank=True)
    tracknumber = models.IntegerField(null=True, blank=True)
    length = models.DecimalField(null=True, max_digits=14, decimal_places=4, blank=True)
    original_length = models.IntegerField(null=True, blank=True)
    license_id = models.IntegerField(null=True, blank=True)
    license_type = models.CharField(max_length=300, blank=True)
    license_source = models.CharField(max_length=300, blank=True)
    license_provider = models.CharField(max_length=300, blank=True)
    license_rights = models.CharField(max_length=750, blank=True)
    license_condition = models.CharField(max_length=750, blank=True)
    license_notes = models.TextField(blank=True)
    tagcomment = models.TextField(blank=True)
    genre = models.CharField(max_length=750, blank=True)
    lyrics = models.TextField(blank=True)
    apid = models.CharField(max_length=450, blank=True)
    xid = models.CharField(max_length=450, blank=True)
    encodedby = models.CharField(max_length=750, blank=True)
    copyright = models.CharField(max_length=750, blank=True)
    isrc = models.CharField(max_length=150, blank=True)
    mediaformat = models.CharField(max_length=36, blank=True)
    mood = models.CharField(max_length=150, blank=True)
    bpm = models.FloatField(null=True, blank=True)
    composer = models.CharField(max_length=750, blank=True)
    lyricist = models.CharField(max_length=750, blank=True)
    remixer = models.CharField(max_length=750, blank=True)
    arranger = models.CharField(max_length=750, blank=True)
    producer = models.CharField(max_length=750, blank=True)
    djmixer = models.CharField(max_length=750, blank=True)
    mixer = models.CharField(max_length=750, blank=True)
    mb_trackid = models.CharField(max_length=108, blank=True)
    mb_releaseid = models.CharField(max_length=108, blank=True)
    mb_artistid = models.CharField(max_length=108, blank=True)
    mb_releaseartistid = models.CharField(max_length=108, blank=True)
    
    wikipedia_url = models.CharField(max_length=750, blank=True)
    soundcloud_url = models.CharField(max_length=750, blank=True)
    youtube_url = models.CharField(max_length=750, blank=True)
    
    musicip_puid = models.CharField(max_length=108, blank=True)
    ofa_fingerprint = models.CharField(max_length=512, blank=True)
    musicmagic_data = models.TextField(blank=True)
    musicmagic_fingerprint = models.TextField(blank=True)
    
    lyricsfly_mediaid = models.CharField(max_length=150, blank=True)
    lyricsfly_status = models.IntegerField()
    
    chartlyrics_status = models.IntegerField()
    tagquality = models.IntegerField(null=True, blank=True)
    orig_title = models.CharField(max_length=750, blank=True)
    orig_artist = models.CharField(max_length=750, blank=True)
    orig_album = models.CharField(max_length=750, blank=True)
    orig_trackno = models.CharField(max_length=9, blank=True)
    sourcepath = models.CharField(max_length=512, blank=True)
    mb_status = models.IntegerField()
    discogs_status = models.IntegerField()
    pipeline_status = models.IntegerField()
    has_flac_default = models.IntegerField()
    has_mp3_default = models.IntegerField()
    cleaned_msg = models.CharField(max_length=150, blank=True)
    cleaned = models.IntegerField()
    mp3_default_length = models.IntegerField(null=True, blank=True)
    has_mp3_64 = models.IntegerField()
    has_mp3_128 = models.IntegerField()
    has_mp3_320 = models.IntegerField()
    has_peakfile = models.IntegerField()
    has_peakfile_raw = models.IntegerField()
    has_peakfile_mp3 = models.IntegerField()
    has_graph = models.IntegerField()
    lock = models.IntegerField()
    autopublish = models.IntegerField()
    migrated = models.DateTimeField(null=True, blank=True)
    total_downloads = models.IntegerField()
    total_plays = models.IntegerField()
    class Meta:
        db_table = u'medias'

class Ntags(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=750, blank=True)
    release_count = models.IntegerField()
    media_count = models.IntegerField()
    label_count = models.IntegerField()
    artist_count = models.IntegerField()
    transmission_count = models.IntegerField()
    playlist_count = models.IntegerField()
    class Meta:
        db_table = u'ntags'

class Playlists(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=750, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    status = models.IntegerField()
    type = models.CharField(max_length=30, blank=True)
    editable = models.IntegerField()
    owner = models.IntegerField(null=True, blank=True)
    access_read = models.CharField(max_length=1536, blank=True)
    access_write = models.CharField(max_length=1536, blank=True)
    editor = models.IntegerField(null=True, blank=True)
    last_updater = models.IntegerField(null=True, blank=True)
    edits = models.IntegerField()
    rev = models.IntegerField()
    last_edit = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    intro = models.CharField(max_length=3072, blank=True)
    notes = models.TextField(blank=True)
    duration = models.IntegerField()
    total_medias = models.IntegerField()
    target_duration = models.IntegerField()
    broadcast_segments = models.CharField(max_length=1536, blank=True)
    rotation_include = models.IntegerField(null=True, blank=True)
    played = models.IntegerField()
    subtype = models.CharField(max_length=30)
    lock = models.IntegerField()
    legacy_id = models.IntegerField()
    class Meta:
        db_table = u'playlists'

class Releases(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=750, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=60)
    editable = models.IntegerField()
    owner = models.CharField(max_length=750, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    edits = models.IntegerField()
    barcode = models.IntegerField(null=True, blank=True)
    asin = models.CharField(max_length=150, blank=True)
    catalognumber = models.CharField(max_length=150, blank=True)
    mb_releaseid = models.CharField(max_length=108, blank=True)
    mb_releaseartistid = models.CharField(max_length=108, blank=True)
    albumartist = models.CharField(max_length=750, blank=True)
    albumartistsortorder = models.CharField(max_length=750, blank=True)
    releasedate = models.CharField(max_length=30, blank=True)
    recordlabel = models.CharField(max_length=750, blank=True)
    releasecountry = models.CharField(max_length=150, blank=True)
    releasestatus = models.CharField(max_length=60, blank=True)
    releasetype = models.CharField(max_length=60, blank=True)
    recording_date = models.DateTimeField(blank=True, null=True)
    event_location = models.CharField(max_length=750, blank=True)
    event_location_town = models.CharField(max_length=750, blank=True)
    event_location_url = models.CharField(max_length=750, blank=True)
    totaltracks = models.IntegerField(null=True, blank=True)
    availabletracks = models.IntegerField(null=True, blank=True)
    parentdirectory = models.CharField(max_length=750, blank=True)
    license_id = models.IntegerField(null=True, blank=True)
    license_type = models.CharField(max_length=300, blank=True)
    license_source = models.CharField(max_length=300, blank=True)
    license_provider = models.CharField(max_length=300, blank=True)
    license_rights = models.CharField(max_length=750, blank=True)
    license_conditions = models.CharField(max_length=750, blank=True)
    license_notes = models.TextField(blank=True)
    tagquality = models.IntegerField(null=True, blank=True)
    pipeline_status = models.IntegerField(blank=True)
    discogs_releaseid = models.CharField(max_length=750, blank=True)
    discogs_status = models.IntegerField(blank=True)
    mb_status = models.IntegerField(blank=True)
    mb_score = models.IntegerField(null=True, blank=True)
    wikipedia_url = models.CharField(max_length=750, blank=True)
    myspace_url = models.CharField(max_length=750, blank=True)
    facebook_url = models.CharField(max_length=750, blank=True)
    release_url = models.CharField(max_length=750, blank=True)
    download_url = models.CharField(max_length=750, blank=True)
    lastfm_url = models.CharField(max_length=750, blank=True)
    various_links = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    has_image = models.IntegerField(null=True, blank=True)
    genres = models.CharField(max_length=750, blank=True)
    styles = models.CharField(max_length=750, blank=True)
    lock = models.IntegerField(null=True, blank=True)
    import_match = models.CharField(max_length=36, blank=True)
    autopublish = models.IntegerField(blank=True)
    migrated = models.DateTimeField(null=True, blank=True)
    total_downloads = models.IntegerField(blank=True)
    total_plays = models.IntegerField(blank=True)
    status_viral = models.IntegerField(blank=True)
    class Meta:
        db_table = u'releases'





class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    legacy_id = models.IntegerField()
    email = models.CharField(max_length=381)
    username = models.CharField(max_length=96, unique=True)
    password = models.CharField(max_length=150)
    full_name = models.CharField(max_length=384, blank=True)
    fb_id = models.CharField(max_length=90, blank=True)
    fb_token = models.CharField(max_length=3072, blank=True)
    logins = models.IntegerField()
    last_login = models.IntegerField(null=True, blank=True)
    client_ip = models.CharField(max_length=45, blank=True)
    class Meta:
        db_table = u'users'














class ArtistsMedias(models.Model):
    id = models.IntegerField(primary_key=True)
    media = models.ForeignKey(Medias)
    artist = models.ForeignKey(Artists)
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'artists_medias'

class ArtistsReleases(models.Model):
    id = models.IntegerField(primary_key=True)
    release = models.ForeignKey(Releases)
    artist = models.ForeignKey(Artists)
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'artists_releases'


class NtagsArtists(models.Model):
    id = models.IntegerField(primary_key=True)
    ntag_id = models.IntegerField()
    artist_id = models.IntegerField()
    created = models.DateTimeField()
    class Meta:
        db_table = u'ntags_artists'

class NtagsLabels(models.Model):
    id = models.IntegerField(primary_key=True)
    ntag_id = models.IntegerField()
    label_id = models.IntegerField()
    created = models.DateTimeField()
    class Meta:
        db_table = u'ntags_labels'

class NtagsMedias(models.Model):
    id = models.IntegerField(primary_key=True)
    ntag_id = models.IntegerField()
    media_id = models.IntegerField()
    created = models.DateTimeField()
    class Meta:
        db_table = u'ntags_medias'

class NtagsPlaylists(models.Model):
    id = models.IntegerField(primary_key=True)
    ntag_id = models.IntegerField()
    playlist_id = models.IntegerField()
    created = models.DateTimeField()
    class Meta:
        db_table = u'ntags_playlists'

class NtagsReleases(models.Model):
    id = models.IntegerField(primary_key=True)
    ntag_id = models.IntegerField()
    release_id = models.IntegerField()
    created = models.DateTimeField()
    class Meta:
        db_table = u'ntags_releases'

class NtagsTransmissions(models.Model):
    id = models.IntegerField(primary_key=True)
    ntag_id = models.IntegerField()
    transmission_id = models.IntegerField()
    created = models.DateTimeField()
    class Meta:
        db_table = u'ntags_transmissions'

class MediasPlaylists(models.Model):
    id = models.IntegerField(primary_key=True)
    media_id = models.IntegerField()
    playlist_id = models.IntegerField()
    created = models.DateTimeField()
    pos = models.IntegerField()
    fade_in = models.IntegerField()
    fade_out = models.IntegerField()
    fade_cross = models.IntegerField()
    cue_in = models.IntegerField()
    cue_out = models.IntegerField()
    class Meta:
        db_table = u'medias_playlists'

class MediasReleases(models.Model):
    id = models.IntegerField(primary_key=True)
    media = models.ForeignKey(Medias)
    release = models.ForeignKey(Releases)
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'medias_releases'

class LabelsReleases(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.ForeignKey(Labels)
    release = models.ForeignKey(Releases)
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'labels_releases'