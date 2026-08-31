import subprocess
import logging

from nunjucks import settings as nunjucks_settings

log = logging.getLogger(__name__)


class NunjucksCompiler:
    def __init__(self):
        pass

    def compile_template(self, path):

        template = ""
        command = f"{nunjucks_settings.NUNJUCKS_BIN} {path}"

        p = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        for line in p.stdout.readlines():
            template += line.decode("utf-8")

        p.wait()

        return template
