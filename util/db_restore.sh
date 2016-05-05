#!/bin/sh

mysql -u root -proot org_openbroadcast_local < ~/code/openbroadcast.org/db_dumps/org_openbroadcast_local.sql
redis-cli flushall
