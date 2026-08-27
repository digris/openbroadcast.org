# replace user model

steps to be done to replace user model:

 - make sure all migrations are applied, except account/0001_initial
 - delete migration history (DELETE FROM `django_migrations`;)
 - fake migrations: ./manage.py migrate --fake
 - update content types: (auth/user tp account/user)
