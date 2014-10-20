import string
import unicodedata

VALID_CHARS = "-_.()[] %s%s" % (string.ascii_letters, string.digits)
EXCLUDE_CHARS = "/\\'"

def safe_name(str):

    #str = str.encode('ascii', 'replace')

    # str = unicodedata.normalize('NFKD', str).encode('ASCII', 'ignore')
    str = unicodedata.normalize('NFKD', str)


    return ''.join(ch for ch in str if ch not in EXCLUDE_CHARS)

    #return ''.join(c for c in str if c in VALID_CHARS)
