#!/usr/bin/env python
from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib import files

import urllib2
import sys


# glogal env
env.warn_only = True
env.supervisor = '/etc/supervisor/conf.d'
env.nginx = '/etc/nginx/sites-enabled'

# skip functions for faster deploy...
env.skip_requirements = False
env.skip_db = False
env.reboot = False

def skip_req():
    env.skip_requirements = True

def skip_db():
    env.skip_db = True

def reboot():
    env.reboot = True


def stage_openbroadcast_ch():
    env.site_id = 'openbroadcast.org'
    env.hosts = ['172.20.10.204']
    env.git_url = 'git@lab.hazelfire.com:hazelfire/obp/openbroadcast-ch.git'
    env.git_branches = ['development', 'master',]
    env.git_default_branch = 'development'
    env.path = '/var/www/openbroadcast.org'
    env.storage = '/nas/storage/stage.openbroadcast.org'
    env.user = 'root'

def prod_openbroadcast_ch():
    env.site_id = 'openbroadcast.org'
    env.hosts = ['172.20.10.205',]
    env.git_url = 'git@lab.hazelfire.com:hazelfire/obp/openbroadcast-ch.git'
    env.git_branches = ['development', 'master',]
    env.git_default_branch = 'development'
    env.path = '/var/www/openbroadcast.org'
    env.storage = '/nas/storage/prod.openbroadcast.org'
    env.user = 'root'



# helpers
def clean():
    local("find . -name '*.DS_Store' -type f -delete")
    local("find . -name '*.pyc' -type f -delete")

def mount():
    local_dir = '~/sshfs/%s' % env.site_id
    try:
        local('mkdir %s' % local_dir)
    except:
        pass

    local('sshfs root@%s:%s %s' % (env.hosts[0], env.path, local_dir))
    local('open %s' % local_dir)


# base deploy
def deploy(branch=None):

    if not branch:
        branch = env.git_default_branch

    if not branch in env.git_branches:
        print 'INVALID BRANCH. EXIT!'
        sys.exit(1)


    try:
        run('mkdir -p %s' % env.path)
    except Exception, e:
        print 'unable to mkdir: %s - %s' % (env.path, e)


    repository_exists = False

    with cd(env.path):  
        
        # create directory to save the local_config
        try:
            run('mkdir config')
        except Exception, e:
            pass
        
        try:
            run('cp src/website/local_settings.py config/')
        except Exception, e:
            pass


        if(files.exists('repository')):
            repository_exists = True

        if not repository_exists:
            try:
                run('rm -Rf src_new')
            except Exception, e:
                pass
            run('mkdir src_new')


    if repository_exists:
        run('cp -Rp repository src_new')

        with cd(env.path + '/repository'):
            print '------------------------------------------'
            run('git pull origin %s' % (branch))
            print '------------------------------------------'

        with cd(env.path):
            run('cp -Rp repository src_new')


    if not repository_exists:

        with cd(env.path + '/src_new'):

            # aquire code from repository
            run('git init')
            run('git remote add -t %s -f origin %s' % (branch, env.git_url))
            run('git fetch')
            run('git checkout %s' % (branch))

        with cd(env.path):
            run('cp -Rp src_new repository')






    with cd(env.path): 

        # copy back the local_settings
        try:
            run('cp config/local_settings.py src_new/website/')
        except Exception, e:
            pass
            
        

        # virtualenv and requirements
        if not env.skip_requirements:

            try:
                run('virtualenv /srv/%s' % env.site_id)
            except Exception, e:
                pass

            try:
                # pip - version < 1.5 needed to allow external modules
                run('/srv/%s/bin/pip install pip==1.4.1' % (env.site_id))
            except Exception, e:
                pass

            try:
                # pre-install numpy, does not work through requirements
                run('/srv/%s/bin/pip install numpy' % (env.site_id))
            except Exception, e:
                pass



            try:
                run('/srv/%s/bin/pip install -r  %s' % (env.site_id, 'src_new/website/requirements/requirements.txt'))
            except Exception, e:
                pass

            
        # run migrations / db-updates
        if not env.skip_db:
            try:
                with cd(env.path + '/src/website/'):
                    run('/srv/%s/bin/python /%s/src_new/website/manage.py syncdb' % (env.site_id, env.path))
                    run('/srv/%s/bin/python /%s/src_new/website/manage.py migrate' % (env.site_id, env.path))
            except Exception, e:
                pass

        # linking storage directories
        try:
            run('ln -s %s/media %s/src_new/website/media' % (env.storage, env.path))
            run('ln -s %s/smedia %s/src_new/website/smedia' % (env.storage, env.path))
            run('ln -s %s/static %s/src_new/website/static' % (env.storage, env.path))
        except Exception, e:
            pass
            

        # staticfiles
        try:
            with cd(env.path + '/src_new/website/site-static/'):
                pass
                #run('rm -R css/*')
                #run('/var/lib/gems/1.8/gems/compass-0.11.7/bin/compass compile -c config-production.rb')
        except Exception, e:
            pass        

        # compress
        try:
            run('/srv/%s/bin/python /%s/src_new/website/manage.py collectstatic --noinput --verbosity=0' % (env.site_id, env.path))
            run('/srv/%s/bin/python /%s/src/website/manage.py compress -f --verbosity=0' % (env.site_id, env.path))
        except Exception, e:
            pass


        # generate git changelog
        try:
            with cd(env.path + '/src_new/website/'):
                run('git log > changelog.txt')
        except Exception, e:
            pass


        # copy documentation
        try:
            run('cp -R %s/src_new/doc/_build/html %s/doc' % (env.path, env.storage))
        except Exception, e:
            pass



        """
        everything should be ready now, so directories can be swapped
        """

        # swap directories
        with cd(env.path):
            try:
                run('mv src src_old')
            except Exception, e:
                print e
            try:
                run('mv src_new src')
            except Exception, e:
                print e

        """
        # linking config files
        try:
            run('rm %s/%s.conf' % (env.supervisor, env.site_id))
            run('ln -s %s/src/conf/%s.supervised.conf %s/%s.conf' % (env.path, env.site_id, env.supervisor, env.site_id))
        except Exception, e:
            pass

        # additional configs
        try:
            run('rm %s/%s' % (env.nginx, env.site_id))
            run('ln -s %s/src/conf/%s.nginx.conf %s/%s' % (env.path, env.site_id, env.nginx, env.site_id))
        except Exception, e:
            pass
        """

        # restart app-server

        if not env.reboot:

            try:
                run('supervisorctl restart %s' % env.site_id)
            except Exception, e:
                print '!!!!!! APP-SERVER WARNING !!!!!!!'
                print e
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'


            # reload_gunicorn()
            restart_services()

        # cleanup
        with cd(env.path):
            try:
                run('rm -R src_old')
            except Exception, e:
                print e

        if env.reboot:
            run('shutdown -r now')


def reload_gunicorn():

    try:
        r = run('supervisorctl status %s' % env.site_id)
        pid = r.split()[3].rstrip(', ')
        pid = int(pid)
        print 'PID: %s' % pid
        run('kill -s HUP %s' % pid)

    except Exception, e:
        print '!!!!!!!!! WARNING !!!!!!!!!!!!!'
        print 'unable to send HUP to gunicorn'
        print e
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'


def restart_services():
    try:
        run('supervisorctl stop services.%s:*' % env.site_id)
        run('supervisorctl reread')
        run('supervisorctl update')
        run('supervisorctl restart services.%s:*' % env.site_id)
    except Exception, e:
        print '!!!!!! SERVICES WARNING !!!!!!!'
        print e
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'



"""
translation related
TODO: adapt configuration for project!
"""

def tx_make():

    """
    on a fresh project first run (for all locales.tx):
    django-admin.py makemessages -l en --all
    """

    local('cd website && django-admin.py makemessages --all \
           --no-obsolete \
           --domain=django \
           --ignore=*admin* \
           --ignore=*filer* \
           --ignore=*l10n* \
           --ignore=*cms_plugins* \
           --ignore=*shop/models/defaults* \
           --ignore=*shop_secondary_currencies* \
           --ignore=*paypal/pro* \
           --ignore=*multilingual* \
           --ignore=*newsletter* \
           --ignore=*cmsplugin_facebook* \
           --ignore=*cmsplugin_youtube* \
           --ignore=*cmsplugin_vimeo* \
           --ignore=*partner/models* \
           --ignore=*atoz/models* \
           --ignore=*faq/models* \
           --ignore=*taggit* \
           --ignore=*cms/* \
           --ignore=*userena/* \
           --ignore=*socialregistration/* \
           --ignore=ajax/* \
           --ignore=analytics/* \
           --ignore=dev/* \
           --ignore=fixtures/* \
           --ignore=registration/* \
           --ignore=lib/* \
           --ignore=locale/* \
           --ignore=media/* \
           --ignore=multilingual/* \
           --ignore=profiles/* \
           --ignore=social_auth/* \
           --ignore=taggit/* \
           --ignore=socialregistration/* \
           --ignore=filer/*')


def tx_push():
    local('tx push -t -s')


def tx_pull(remote=False):

    local('tx pull')
    local('cd website && ./manage.py compilemessages')


def tx_pull_remote():

    with cd(env.path + '/src'):
        run('tx pull')
    with cd(env.path + '/src/website'):
        run('/srv/%s/bin/python /%s/src/website/manage.py compilemessages' % (env.site_id, env.path))


