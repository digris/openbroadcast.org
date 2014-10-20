"""alibrary - default settings"""
from django.conf import settings
from django.utils.translation import ugettext as _





"""
Release choices
"""
DEFAULT_RELEASETYPE_CHOICES = (
    (_('General'), (
            ('album', _('Album')),
            ('single', _('Single')),
            ('ep', _('EP')),
            ('compilation', _('Compilation')),
            ('soundtrack', _('Soundtrack')),
            ('audiobook', _('Audiobook')),
            ('spokenword', _('Spokenword')),
            ('interview', _('Interview')),
            ('live', _('Live')),
            ('remix', _('Remix')),
            ('broadcast', _('Broadcast')),
            ('djmix', _('DJ-Mix')),
            ('mixtape', _('Mixtape')),
        )
    ),
    #(_('Recording'), (
    #        ('remix', _('Remix')),
    #        ('live', _('Live')),
    #    )
    #),
    ('other', _('Other')),
)

"""
Label choices
"""
DEFAULT_LABELTYPE_CHOICES = (
    ('unknown', _('Unknown')),
    ('major', _('Major Label')),
    ('indy', _('Independent Label')),
    ('net', _('Netlabel')),
    ('event', _('Event Label')),
)


"""
Playlist choices
"""
DEFAULT_PLAYLIST_TARGET_DURATION_CHOICES = (
    (900, '15'),
    (1800, '30'),
    (2700, '45'),
    (3600, '60'),
    (4500, '75'),
    (5400, '90'),
    (6300, '105'),
    (7200, '120'),

    (8100, '135'),
    (9000, '150'),
    (9900, '165'),
    (10800, '180'),
    (11700, '195'),
    (12600, '210'),
    (13500, '225'),
    (14400, '240'),

)
DEFAULT_PLAYLIST_STATUS_CHOICES = (
    (0, _('Init')),
    (1, _('Ready')),
    (2, _('In progress')),
    (3, _('Scheduled')),
    (4, _('Descheduled')),
    (99, _('Error')),
    (11, _('Other')),
)

DEFAULT_PLAYLIST_TYPE_CHOICES = (
    ('basket', _('Private Playlist')),
    ('playlist', _('Public Playlist')),
    ('broadcast', _('Broadcasts')),
    ('other', _('Other')),
)

DEFAULT_PLAYLIST_BROADCAST_STATUS_CHOICES = (
    (0, _('Undefined')),
    (1, _('OK')),
    (2, _('Warning')),
    (99, _('Error')),
)

"""
binaries
"""

LAME_BINARY = getattr(settings, 'LAME_BINARY', '/usr/bin/lame')
SOX_BINARY = getattr(settings, 'SOX_BINARY', '/usr/bin/sox')
FAAD_BINARY = getattr(settings, 'FAAD_BINARY', '/usr/bin/faad')


"""
choice settings
"""

RELEASETYPE_CHOICES = getattr(settings, 'ALIBRARY_RELEASETYPE_CHOICES', DEFAULT_RELEASETYPE_CHOICES)
LABELTYPE_CHOICES = getattr(settings, 'ALIBRARY_LABELTYPE_CHOICES', DEFAULT_LABELTYPE_CHOICES)

PLAYLIST_TARGET_DURATION_CHOICES = getattr(settings, 'ALIBRARY_PLAYLIST_TARGET_DURATION_CHOICES', DEFAULT_PLAYLIST_TARGET_DURATION_CHOICES)
PLAYLIST_STATUS_CHOICES = getattr(settings, 'ALIBRARY_PLAYLIST_STATUS_CHOICES', DEFAULT_PLAYLIST_STATUS_CHOICES)
PLAYLIST_TYPE_CHOICES = getattr(settings, 'ALIBRARY_PLAYLIST_TYPE_CHOICES', DEFAULT_PLAYLIST_TYPE_CHOICES)
PLAYLIST_BROADCAST_STATUS_CHOICES = getattr(settings, 'ALIBRARY_PLAYLIST_BROADCAST_STATUS_CHOICES', DEFAULT_PLAYLIST_BROADCAST_STATUS_CHOICES)
