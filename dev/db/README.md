


    # optimize tables / rebuild index
    mysqlcheck org_openbroadcast -u root -p --optimize



## resetting migrations

    ./manage.py migrate --fake alibrary zero
    git mv apps/alibrary/migrations apps/alibrary/old_migrations
    
    ./manage.py makemigrations alibrary
    ./manage.py migrate alibrary --fake-initial


## postgres migration

Make sure all types got updated properly.  
TODO: investigate why `migrations.RunSQL` is not working

    # reset sequences
    ALTER SEQUENCE django_content_type_id_seq RESTART WITH 1;
    UPDATE django_content_type SET id=nextval('django_content_type_id_seq');
    
    ALTER SEQUENCE auth_permission_id_seq RESTART WITH 1;
    UPDATE auth_permission SET id=nextval('auth_permission_id_seq');

    # fix types
    ALTER TABLE alibrary_distributor ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE alibrary_media ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE alibrary_playlist ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE alibrary_playlistitem ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE alibrary_playlistitemplaylist ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE alibrary_release ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE alibrary_series ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE abcast_channel ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE abcast_emission ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE abcast_jingle ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE abcast_onairitem ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE abcast_station ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE alibrary_relation ALTER COLUMN object_id type INTEGER USING object_id::integer;
    ALTER TABLE alibrary_label ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE alibrary_artist ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE massimporter_massimport ALTER COLUMN uuid type uuid USING uuid::uuid;
    ALTER TABLE massimporter_massimportfile ALTER COLUMN uuid type uuid USING uuid::uuid;
