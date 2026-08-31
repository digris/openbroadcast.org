from django.conf import settings

"""
Release choices
"""
DEFAULT_RELEASETYPE_CHOICES = (
    (
        "General",
        (
            ("album", "Album"),
            ("single", "Single"),
            ("ep", "EP"),
            ("compilation", "Compilation"),
            ("soundtrack", "Soundtrack"),
            ("audiobook", "Audiobook"),
            ("spokenword", "Spokenword"),
            ("interview", "Interview"),
            ("jingle", "Jingle"),
            ("live", "Live"),
            ("remix", "Remix"),
            ("broadcast", "Broadcast"),
            ("djmix", "DJ-Mix"),
            ("mixtape", "Mixtape"),
        ),
    ),
    # ('Recording', (
    #        ('remix', 'Remix'),
    #        ('live', 'Live'),
    #    )
    # ),
    ("other", "Other"),
)

"""
Label choices
"""
DEFAULT_LABELTYPE_CHOICES = (
    ("unknown", "Unknown"),
    ("major", "Major Label"),
    ("indy", "Independent Label"),
    ("net", "Netlabel"),
    ("event", "Event Label"),
)


"""
Playlist choices
"""
DEFAULT_PLAYLIST_TARGET_DURATION_CHOICES = (
    (900, "15"),
    (1800, "30"),
    (2700, "45"),
    (3600, "60"),
    (4500, "75"),
    (5400, "90"),
    (6300, "105"),
    (7200, "120"),
    (8100, "135"),
    (9000, "150"),
    (9900, "165"),
    (10800, "180"),
    (11700, "195"),
    (12600, "210"),
    (13500, "225"),
    (14400, "240"),
)
DEFAULT_PLAYLIST_STATUS_CHOICES = (
    (0, "Init"),
    (1, "Ready"),
    (2, "In progress"),
    (3, "Scheduled"),
    (4, "Descheduled"),
    (99, "Error"),
    (11, "Other"),
)

# DEFAULT_PLAYLIST_TYPE_CHOICES = (
#     ('basket', 'Private Playlist'),
#     ('playlist', 'Public Playlist'),
#     ('broadcast', 'Broadcasts'),
#     ('other', 'Other'),
# )

DEFAULT_PLAYLIST_BROADCAST_STATUS_CHOICES = (
    (0, "Undefined"),
    (1, "OK"),
    (2, "Warning"),
    (99, "Error"),
)

DEFAULT_ARTIST_JOIN_PHRASE_CHOICES = (
    ("&", "&"),
    (",", ","),
    ("and", "and"),
    ("feat", "feat."),
    ("feat.", "feat."),
    ("presents", "presents"),
    ("meets", "meets"),
    ("with", "with"),
    ("vs", "vs."),
    ("x", "X"),
    ("-", "-"),
)


# choice settings
# TODO: where possible implement choices directly in models
RELEASETYPE_CHOICES = getattr(
    settings, "ALIBRARY_RELEASETYPE_CHOICES", DEFAULT_RELEASETYPE_CHOICES
)
LABELTYPE_CHOICES = getattr(
    settings, "ALIBRARY_LABELTYPE_CHOICES", DEFAULT_LABELTYPE_CHOICES
)

PLAYLIST_TARGET_DURATION_CHOICES = getattr(
    settings,
    "ALIBRARY_PLAYLIST_TARGET_DURATION_CHOICES",
    DEFAULT_PLAYLIST_TARGET_DURATION_CHOICES,
)
PLAYLIST_STATUS_CHOICES = getattr(
    settings, "ALIBRARY_PLAYLIST_STATUS_CHOICES", DEFAULT_PLAYLIST_STATUS_CHOICES
)
# PLAYLIST_TYPE_CHOICES = getattr(
#     settings,
#     'ALIBRARY_PLAYLIST_TYPE_CHOICES',
#     DEFAULT_PLAYLIST_TYPE_CHOICES
# )
PLAYLIST_BROADCAST_STATUS_CHOICES = getattr(
    settings,
    "ALIBRARY_PLAYLIST_BROADCAST_STATUS_CHOICES",
    DEFAULT_PLAYLIST_BROADCAST_STATUS_CHOICES,
)
ARTIST_JOIN_PHRASE_CHOICES = getattr(
    settings, "ALIBRARY_ARTIST_JOIN_PHRASE_CHOICES", DEFAULT_ARTIST_JOIN_PHRASE_CHOICES
)
