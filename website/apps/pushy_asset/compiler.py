import subprocess

PUSHY_ASSET_BIN = '/opt/local/bin/pushy_asset-precompile'

"""
Just a wrapper to the pushy_asset/npm 'binary'
"""

class PushyAssetCompiler(object):

    def __init__(self):
        pass


    def compile(self, path):

        template = ''
        command = '%s %s' % (PUSHY_ASSET_BIN, path)
        print command
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            template += line
        retval = p.wait()


        return template