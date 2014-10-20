import subprocess

NUNJUCKS_BIN = '/opt/local/bin/nunjucks-precompile'

"""
Just a wrapper to the nunjucks/npm 'binary'
"""

class NunjucksCompiler(object):

    def __init__(self):
        pass


    def compile(self, path):

        template = ''
        command = '%s %s' % (NUNJUCKS_BIN, path)
        print command
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            template += line
        retval = p.wait()


        return template