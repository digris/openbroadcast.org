import datetime
import os

from django.utils.encoding import force_unicode, smart_str

from filer.utils.files import get_valid_filename


def by_date(instance, filename):
    datepart = force_unicode(datetime.datetime.now().strftime(smart_str("%Y/%m/%d")))
    return os.path.join(datepart, get_valid_filename(filename))
