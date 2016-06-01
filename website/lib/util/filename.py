import string

from lib.util.AsciiDammit import asciiDammit

VALID_CHARS = "-_.()[] %s%s" % (string.ascii_letters, string.digits)
EXCLUDE_CHARS = "/\\'"

def safe_name(str):

    return asciiDammit(str.replace('/', ' '))
