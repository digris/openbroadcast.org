from __future__ import absolute_import


def update_permissions_after_migration(app,**kwargs):

    from django.conf import settings
    from django.db.models import get_app, get_models
    from django.contrib.auth.management import create_permissions

    create_permissions(get_app(app), get_models(), 2 if settings.DEBUG else 0)

#post_migrate.connect(update_permissions_after_migration)



