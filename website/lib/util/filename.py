import string
import unicodedata

from lib.util.AsciiDammit import asciiDammit

VALID_CHARS = "-_.()[] %s%s" % (string.ascii_letters, string.digits)
EXCLUDE_CHARS = "/\\'"

def safe_name(str):

    return asciiDammit(str.replace('/', ' '))

    str = unicodedata.normalize('NFKD', str)

    return ''.join(ch for ch in str if ch not in EXCLUDE_CHARS)
