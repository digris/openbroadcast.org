from collections import defaultdict

from django.db import connection, transaction
from django.core.management.base import BaseCommand
from south.db import db

from datatrans.models import KeyValue


class Command(BaseCommand):
    help = 'Deletes duplicate KeyValues, only mysql is supported in a fast way'

    @transaction.commit_on_success
    def remove_duplicates_mysql(self):
        """
        Removes all the duplicates from the datatrans_keyvalue table. First we detect what the most horrible
        duplication count is of a KeyValue.  Then we iterate through the count and start deleting the newest duplicate
        row of a certain KeyValue.  Wow, confused?

        The majority of KeyValues have 1 duplication, but some have 2 duplications. This means that we have to execute
        the deletion query twice since it only deletes 1 duplication (the newest) each time
        """
        print '  Deleting duplicates from datatrans_keyvalue table'
        cursor = connection.cursor()
        cursor.execute("""
            select count(id)
            from datatrans_keyvalue
            group by digest, language, content_type_id, object_id, field
            having count(*) > 1
            order by count(id) desc
        """)
        row = cursor.fetchone()

        if row and row[0] > 0:
            count = row[0]
            print '   - Most horrible duplication count = ', count

            for i in range(count - 1):
                # Mysql doesn't allow to delete in a table while fetching values from it (makes sense).
                # Therefore we have to fetch the duplicate ids first into a python list.
                # Secondly we pass this list to the deletion query
                print '   - Deleting entries with %s duplicates' % (i + 1)
                cursor.execute("""
                        select max(id)
                        from datatrans_keyvalue
                        group by digest, language, content_type_id, object_id, field
                        having count(*) > 1
                    """)

                ids = [str(_row[0]) for _row in cursor.fetchall()]
                strids = ",".join(ids)

                cursor.execute("""
                    delete from datatrans_keyvalue
                    where id in (%s)
                """ % strids)
        else:
            print '   - No duplicates found'

    def remove_duplicates_default(self):
        """
        A cleaner implementation. But unfortunately way more slower slower
        """
        kv_map = defaultdict(lambda: [])
        deleted = 0

        for kv in KeyValue.objects.all():
            # For some reason a null object exists in the database
            if not kv.id:
                continue

            key = (kv.language, kv.digest, kv.content_type, kv.object_id, kv.field)
            kv_map[key].append(kv)

            for (kv.language, kv.digest, kv.content_type, kv.object_id, kv.field), kv_list in kv_map.items():
                if len(kv_list) == 1:
                    continue

                kv_list.sort(key=lambda kv: kv.id)

                for kv in kv_list[:-1]:
                    if kv.id:
                        print 'Deleting KeyValue ', kv.id, ", ", kv
                        deleted += 1
                        kv.delete()

        print 'Duplicates deleted:', deleted

    def print_db_info(self):
        from django.conf import settings
        conn = db._get_connection().connection
        dbinfo = settings.DATABASES[db.db_alias]
        print 'Database: ' + conn.get_host_info() + ":" + str(conn.port) + ", db: " + dbinfo['NAME']

    def handle(self, *args, **options):
        self.print_db_info()

        if db.backend_name == 'mysql':
            print 'Remove duplicates: mysql'
            self.remove_duplicates_mysql()
        else:
            #print 'Remove duplicates: default'
            #print 'Grab some coffee, this can take a while ...'
            #self.remove_duplicates_default()
            print 'Unfortunately this command only supports mysql, selected db: ', db.backend_name
