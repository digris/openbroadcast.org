#!/bin/sh

mysqldump -u root -proot org_openbroadcast_local_rebuild > ~/code/openbroadcast.org/util/db/dump_mysql/org_openbroadcast_local_rebuild.sql
