# uninstall
pip uninstall django-modeltranslation
pip uninstall south




# migration steps

./manage.py migrate --fake-initial

delete all cms tables


/* 11:31:54 localhost */ SET FOREIGN_KEY_CHECKS = 0;
/* 11:31:54 localhost */ DROP TABLE `cms_title`;
/* 11:31:54 localhost */ DROP TABLE `cms_placeholder`;
/* 11:31:54 localhost */ DROP TABLE `cms_pageusergroup`;
/* 11:31:54 localhost */ DROP TABLE `cms_pageuser`;
/* 11:31:54 localhost */ DROP TABLE `cms_pagepermission`;
/* 11:31:54 localhost */ DROP TABLE `cms_pagemoderatorstate`;
/* 11:31:54 localhost */ DROP TABLE `cms_pagemoderator`;
/* 11:31:54 localhost */ DROP TABLE `cms_page_placeholders`;
/* 11:31:54 localhost */ DROP TABLE `cms_page`;
/* 11:31:54 localhost */ DROP TABLE `cms_globalpagepermission_sites`;
/* 11:31:54 localhost */ DROP TABLE `cms_globalpagepermission`;
/* 11:31:54 localhost */ DROP TABLE `cms_cmsplugin`;
/* 11:31:54 localhost */ SET FOREIGN_KEY_CHECKS = 1;



delete cms migration entries

/* 11:32:39 localhost */ DELETE FROM `south_migrationhistory` WHERE `app_name` = 'cms';




./manage.py migrate cms


./manage.py migrate django_comments --fake-initial
./manage.py migrate easy_thumbnails 0002 --fake
./manage.py migrate --fake-initial


./manage.py migrate



# sql hacks
/* 14:08:18 localhost */ ALTER TABLE `reversion_version` CHANGE `type` `type` SMALLINT(5)  UNSIGNED  NOT NULL  DEFAULT '1';
/* 17:35:47 localhost */ ALTER TABLE `postman_message` CHANGE `sender_archived` `sender_archived` TINYINT(1)  NULL;
/* 17:35:12 localhost */ ALTER TABLE `postman_message` CHANGE `recipient_archived` `recipient_archived` TINYINT(1)  NULL;


./manage.py loaddata fixtures/cms_initial.json

