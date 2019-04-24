


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





## convert mysql to postgres

    mysqldump --compatible=postgresql --default-character-set=utf8 -r org_openbroadcast_local.mysql -u root -proot org_openbroadcast_local

    ./db_converter.py org_openbroadcast_local.mysql org_openbroadcast_local.psql
    
    
    # replace:  "date_joined" timestamp with time zone NOT NULL > "date_joined" timestamp with time zone NULL
    
    dropdb org_openbroadcast_local
    createdb org_openbroadcast_local
    psql -d org_openbroadcast_local -f org_openbroadcast_local.psql




## clean legacy/leftover tables

    # sessions are stored in redis
    TRUNCATE TABLE `django_session`;
    
    # remove zinnia
    DROP TABLE `zinnia_entry_sites`;
    DROP TABLE `zinnia_entry_related`;
    DROP TABLE `zinnia_entry_categories`;
    DROP TABLE `zinnia_entry_authors`;
    TRUNCATE TABLE `cmsplugin_zinnia_selectedentriesplugin_entries`;
    TRUNCATE TABLE `cmsplugin_zinnia_latestentriesplugin_tags`;
    TRUNCATE TABLE `cmsplugin_zinnia_latestentriesplugin_categories`;
    TRUNCATE TABLE `cmsplugin_zinnia_latestentriesplugin_authors`;
    DROP TABLE `cmsplugin_zinnia_selectedentriesplugin_entries`;
    DROP TABLE `cmsplugin_zinnia_latestentriesplugin_tags`;
    DROP TABLE `cmsplugin_zinnia_latestentriesplugin_categories`;
    DROP TABLE `cmsplugin_zinnia_latestentriesplugin_authors`;
    TRUNCATE TABLE `zinnia_entry`;
    TRUNCATE TABLE `zinnia_category`;
    DROP TABLE `zinnia_entry`;
    DROP TABLE `zinnia_category`;
    
    DROP TABLE `announcements_dismissal`;
    DROP TABLE `announcements_announcement`;
    
    DROP TABLE `ashop_hardwarerelease`;
    DROP TABLE `ashop_downloadrelease`;
    DROP TABLE `ashop_downloadmedia`;
    DROP TABLE `ashop_releaseproduct`;
    
    DROP TABLE `apiv1cache_resourcemap`;
    
    TRUNCATE TABLE `backfeed_backfeed`;
    TRUNCATE TABLE `backfeed_backfeed`;
    DROP TABLE `backfeed_backfeed`;
    
    DROP TABLE `cmsplugin_channelplugin`;
    
    TRUNCATE TABLE `bcmon_playout`;
    DROP TABLE `bcmon_channel`;
    
    DELETE FROM `bcmon_channel` WHERE `id` > 0;
    TRUNCATE TABLE `bcmon_channel`;
    DROP TABLE `bcmon_channel`;
    
    DROP TABLE `cmsplugin_artistplugin`;
    DROP TABLE `cmsplugin_calendarentriesplugin`;
    DROP TABLE `cmsplugin_latestentriesplugin`;
    DROP TABLE `cmsplugin_mediaplugin`;
    DROP TABLE `cmsplugin_queryentriesplugin`;
    DROP TABLE `cmsplugin_randomentriesplugin`;
    DROP TABLE `cmsplugin_releaseplugin`;
    DROP TABLE `cmsplugin_selectedentriesplugin`;
    
    DROP TABLE `datatrans_modelwordcount`;
    DROP TABLE `datatrans_keyvalue`;
    DROP TABLE `datatrans_fieldwordcount`;
    
    DROP TABLE `eav_value`;
    DROP TABLE `eav_enumgroup_enums`;
    DROP TABLE `eav_attribute`;
    DROP TABLE `eav_enumvalue`;
    DROP TABLE `eav_enumgroup`;
    
    DROP TABLE `guardian_userobjectpermission`;
    DROP TABLE `guardian_groupobjectpermission`;
    
    DROP TABLE `paypal_ipn`;
    
    TRUNCATE TABLE `cmsplugin_shortcutplugin`;
    DROP TABLE `cmsplugin_shortcutplugin`;
    DELETE FROM `shortcutter_shortcut` WHERE `id` > 0;
    DELETE FROM `shortcutter_shortcutcollection` WHERE `id` > 0;
    DROP TABLE `shortcutter_shortcut`;
    DROP TABLE `shortcutter_shortcutcollection`;
    DROP TABLE `shortcutter_shortcut`;
    DROP TABLE `shortcutter_shortcutcollection`;
    
    DROP TABLE `shop_orderpayment`;
    DROP TABLE `shop_orderextrainfo`;
    DROP TABLE `shop_extraorderpricefield`;
    DROP TABLE `shop_extraorderitempricefield`;
    DROP TABLE `shop_cartitem`;
    DROP TABLE `shop_cart`;
    
    DROP TABLE `shop_orderitem`;
    DROP TABLE `shop_order`;
    DROP TABLE `shop_product`;
    
    TRUNCATE TABLE `spf_request`;
    TRUNCATE TABLE `spf_match`;
    DROP TABLE `spf_match`;
    DROP TABLE `spf_request`;
    
    DROP TABLE `subscription_subscriptionbuttonplugin`;
    DROP TABLE `subscription_subscription`;
    DROP TABLE `subscription_newsletter_translation`;
    DROP TABLE `subscription_newsletter`;
    
    DROP TABLE `cmsplugin_pagedownconfig`;

    ALTER TABLE `auth_user` CHANGE `date_joined` `date_joined` DATETIME  NULL  DEFAULT NULL;
    DROP TABLE `cmsplugin_guideplugin`;
