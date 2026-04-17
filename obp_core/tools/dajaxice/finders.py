import os
import tempfile

from django.contrib.staticfiles import finders
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from django.core.exceptions import SuspiciousOperation


class VirtualStorage(FileSystemStorage):
    """
    Mock a FileSystemStorage to build temporary files on demand.
    """

    def __init__(self, *args, **kwargs):
        super(VirtualStorage, self).__init__(*args, **kwargs)
        self._files_cache = {}

    def get_or_create_file(self, path):
        if path not in self.files:
            return ""

        generator = getattr(self, self.files[path])
        data = generator()

        try:
            cached_path = self._files_cache[path]
            with open(cached_path, "r") as f:
                current_data = f.read()
            if current_data != data:
                raise ValueError("Cached data mismatch")
        except Exception:
            fd, tmp_path = tempfile.mkstemp()
            with os.fdopen(fd, "w") as tmp_file:
                tmp_file.write(data)
            self._files_cache[path] = tmp_path

        return self._files_cache[path]

    def exists(self, name):
        return name in self.files

    def listdir(self, path):
        folders, files = [], []
        for f in self.files:
            if f.startswith(path):
                remainder = f[len(path):].lstrip(os.sep)
                if os.sep in remainder:
                    folders.append(remainder.split(os.sep, 1)[0])
                else:
                    files.append(remainder)
        return folders, files

    def path(self, name):
        try:
            path = self.get_or_create_file(name)
        except Exception:
            raise SuspiciousOperation(
                "Attempted access to '%s' denied." % name
            )
        return os.path.normpath(path)


class DajaxiceStorage(VirtualStorage):
    """
    Dynamic storage for dajaxice-generated JS.
    """

    files = {
        os.path.join("dajaxice", "dajaxice.core.js"): "dajaxice_core_js",
    }

    def dajaxice_core_js(self):
        from dajaxice.core import dajaxice_autodiscover, dajaxice_config

        dajaxice_autodiscover()

        return get_template(
            os.path.join("dajaxice", "dajaxice.core.js")
        ).render(
            {
                "dajaxice_config": dajaxice_config,
            }
        )


class DajaxiceFinder(finders.BaseStorageFinder):
    """
    Staticfiles finder for dynamically generated dajaxice assets.
    """

    storage = DajaxiceStorage()
