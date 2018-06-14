#!/bin/sh

dropdb org_openbroadcast_local_rebuild
createdb org_openbroadcast_local_rebuild
#pg_restore --clean --no-acl --no-owner -d org_openbroadcast_local_rebuild ~/code/openbroadcast.org/util/db/dump_psql/org_openbroadcast_local_rebuild.sql
psql -d org_openbroadcast_local_rebuild -f ~/code/openbroadcast.org/util/db/dump_psql/org_openbroadcast_local_rebuild.sql
