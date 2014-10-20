import re

def generate_settings(channel):
    
    """
    defined here hard-coded, think about where to get the info from
    """
    
    off_air_meta = "%s - offline" % channel.name
    
    
    master_live_stream_port = 0
    master_live_stream_mp = ""
    dj_live_stream_port = 0
    dj_live_stream_port = ""
    
    
    settings = {}
    """
    global settings
    """
    settings['off_air_meta'] = u'%s - OFF-AIR' % channel.name
    settings['output_sound_device'] = False
    settings['output_sound_device_type'] = 'ALSA'
    settings['icecast_vorbis_metadata'] = True
    
    settings['master_live_stream_port'] = 0
    settings['master_live_stream_mp'] = ''
    settings['dj_live_stream_port'] = 0
    settings['dj_live_stream_mp'] = ''
    
    """
    per stream / format settings
    """

    server = channel.stream_server
    
    print server
    print 'server name: %s' % server.name
    print 'host:        %s' % server.host
    print 'admin:       %s' % server.admin_pass
    print 'formats:     %s' % server.formats.all()
    print 'mount:       %s' % channel.mount
    

    
    for i in (0,1,2):
        try:
            format = server.formats.all()[i]
        except Exception, e:
            format = None
            
        """
        s1_enable = true
        s1_output = "icecast"
        s1_type = "mp3"
        s1_bitrate = 256
        s1_host = "localhost"
        s1_port = 8000
        s1_user = ""
        s1_pass = "hackme"
        s1_mount = "obp-dev-256.mp3"
        s1_url = "http://airtime.sourcefabric.org"
        s1_description = "Airtime Radio! Stream #1"
        s1_genre = "genre"
        """
            
        if format:
            
            p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
            m = re.search(p, server.host)
            host = m.group('host')
            port = int(m.group('port'))
            
            
            mount = '/%s-%s.%s' % (channel.mount, format.bitrate, format.type)
            print 'got format: %s' % format
            print 'mount:      %s' % mount
            settings['s%s_enable' % (i + 1)]      = True
            settings['s%s_name' % (i + 1)]        = '%s | %s %skbps' % (channel.name, format.get_type_display(), format.bitrate)
            settings['s%s_output' % (i + 1)]      = 'icecast'
            settings['s%s_channels' % (i + 1)]    = 'stereo'
            settings['s%s_type' % (i + 1)]        = format.type
            settings['s%s_bitrate' % (i + 1)]     = format.bitrate
            settings['s%s_host' % (i + 1)]        = host
            settings['s%s_port' % (i + 1)]        = port
            settings['s%s_user' % (i + 1)]        = ''
            settings['s%s_pass' % (i + 1)]        = server.source_pass
            settings['s%s_mount' % (i + 1)]       = mount
            settings['s%s_url' % (i + 1)]         = ''
            settings['s%s_description' % (i + 1)] = channel.teaser
            settings['s%s_genre' % (i + 1)]       = 'Music!'
            
        else:
            print 'not defined, use dummy data and disable'
            settings['s%s_enable' % (i + 1)]      = False
            settings['s%s_name' % (i + 1)]        = ''
            settings['s%s_output' % (i + 1)]      = ''
            settings['s%s_channels' % (i + 1)]    = 'stereo'
            settings['s%s_type' % (i + 1)]        = ''
            settings['s%s_bitrate' % (i + 1)]     = 0
            settings['s%s_host' % (i + 1)]        = ''
            settings['s%s_port' % (i + 1)]        = 0
            settings['s%s_user' % (i + 1)]        = ''
            settings['s%s_pass' % (i + 1)]        = ''
            settings['s%s_mount' % (i + 1)]       = ''
            settings['s%s_url' % (i + 1)]         = ''
            settings['s%s_description' % (i + 1)] = ''
            settings['s%s_genre' % (i + 1)]       = ''
            
        



    
    """
    sorry for hacking here, but else too much rewrite would be needed in airtime/pypo
    mapping values to airtime parser format
    """
    _settings = []
    for key, value in settings.iteritems():
        type = None
        if isinstance(value, basestring):
            type = 'string'
        item = {
                 'keyname': key,
                 'value': str(value),
                 'type': type
                }
        _settings.append(item)
    
    settings = _settings

    return settings




""" /etc/airtime/__liquidsoap.cfg

off_air_meta = "Airtime - offline"
output_sound_device = false
output_sound_device_type = "ALSA"
icecast_vorbis_metadata = false


s1_enable = true
s1_output = "icecast"
s1_type = "mp3"
s1_bitrate = 256
s1_host = "localhost"
s1_port = 8000
s1_user = ""
s1_pass = "hackme"
s1_mount = "obp-dev-256.mp3"
s1_url = "http://airtime.sourcefabric.org"
s1_description = "Airtime Radio! Stream #1"
s1_genre = "genre"



s2_enable = true
s2_output = "icecast"
s2_type = "mp3"
s2_bitrate = 320
s2_host = "localhost"
s2_port = 8000
s2_user = ""
s2_pass = "hackme"
s2_mount = "obp-dev-320.mp3"
s2_url = ""
s2_description = ""
s2_genre = ""
s3_enable = false
s3_output = "icecast"
s3_type = ""
s3_bitrate = 0
s3_host = ""
s3_port = 0
s3_user = ""
s3_pass = ""
s3_mount = ""
s3_url = ""
s3_description = ""
s3_genre = ""
s1_name = "Airtime!"
s2_name = ""
s3_name = ""
s1_channels = "stereo"
s2_channels = "stereo"
s3_channels = "stereo"

master_live_stream_port = 0
master_live_stream_mp = ""
dj_live_stream_port = 0
dj_live_stream_mp = ""
# log_file = "/var/log/pypo/ls/<script>.log"
"""