FORMATS_MEDIA = {
    'mp3': ['base', ],
}


AJAX_LOOKUP_CHANNELS = {
    'aliases': {'model': 'alibrary.artist', 'search_field': 'name'}
}
# AJAX_SELECT_BOOTSTRAP = True
# AJAX_SELECT_INLINES = 'inline'

BLEACH_ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'em', 'strong', 'a']
BLEACH_STRIP_TAGS = True

"""
stream - defaults to: mp3, highest available bitrate.
would theoretically be possible to implement bitrate-switching
depending on users connection.
"""
FORMATS_STREAM = {
    'mp3': [128],
}
FORMATS_DOWNLOAD = {
    'mp3': [192],
    'flac': ['base'],
    'wav': ['base'],
}

WAVEFORM_SIZES = {
    's': [100, 20],
    'm': [300, 30],
    'l': [600, 100],
}





ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_AUTO_SIGNUP = True
EMAIL_CONFIRMATION_DAYS = 5
