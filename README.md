# Open Broadcast - Platform

Music library, playlist management, and broadcast scheduling platform.

## Project

Open Broadcast began as an ambitious community-driven media platform built around music and radio. The original vision went far beyond playlist management and broadcast scheduling: the platform was intended as a shared digital hub for music discovery and archiving, collaborative editorial and journalistic work, radio and audio production, community programming, events, studios, and other forms of participation.

Much of this vision was implemented or experimented with over the project's history, but many parts ultimately proved too complex, did not attract sufficient community participation, or were not sustainable in practice. The scope gradually narrowed to the parts that remained useful and operational.

Today, the surviving platform is primarily an internal tool for managing a music library, creating and curating playlists, and scheduling music for broadcast.

The codebase still carries traces of the broader original vision. Concepts such as fine-grained permissions, different user roles (including the historical "mentor" role), and multi-tenancy were designed for a much larger and more diverse community and organizational model than the platform serves today. Some of these structures remain even though the workflows that originally required them have disappeared or been greatly simplified.

For a detailed account of the original vision and how the project evolved, see [Project History](docs/history/README.md).


(PLACEHOLDER))

## History (Technical)

Here, in the `next` branch, we are attempting to bring the project back into a usable and maintainable state.

The project has been around for a long time and has gone through several major refactoring and migration steps. The timeline below is reconstructed roughly from memory, so take the years with a grain of salt ;)

Only some of the more or less relevant technical information is included here.

* **2008** - PHP / [Elgg ~v1.8](https://github.com/Elgg/Elgg/blob/4.3/CHANGELOG.md#v181b-october-11-2011)  
  Manual CSS, copy-pasted jQuery, all the way.

* **2009** - Added [CodeIgniter](https://www.codeigniter.com/)  
  Used for the music management parts of the platform.

* **2011** - Replaced the frontend with [Kohana](https://kohanaframework.org/)  
  Adopted LESS and Bootstrap 2 for styling.  
  Still kept CodeIgniter and Elgg for editing functionality.

* **2013** - Migrated the backend to [Django](https://www.djangoproject.com/)  
  Removed all PHP code, while temporarily running against legacy databases in parallel for authentication.  
  Frontend/templates were still based on the Kohana version.

* **2014** - Moved the primary UI to SASS / [Foundation](https://get.foundation/)  
  jQuery remained the primary JavaScript library, with partial enhancements using  
  [dajax](https://github.com/jorgebastida/django-dajax) /
  [dajaxice](https://github.com/jorgebastida/django-dajaxice)
  and [Nunjucks](https://mozilla.github.io/nunjucks/).

* **2015** - Added a [Tastypie](https://github.com/django-tastypie/django-tastypie)-based REST API.

* **2016** - Started porting the primary UI to Vue  
  Introduced package management with npm.  
  Still had copy-pasted jQuery and manual CSS scattered throughout the codebase, combined with legacy jQuery version(s).

* **2018** - Introduced Vue Single-File Components (SFCs), along with improved frontend tooling.

* **2019** - Added a [Django REST Framework](https://www.django-rest-framework.org/)-based REST API (v2), alongside the existing Tastypie API.

* **2020 onwards** - Continued improving and adding workflows and features, more or less based on the existing stack.

### Situation (as of 2026)

Over the years, a significant amount of technical debt has accumulated, and the potential scope for cleaning up and modernizing the platform has become rather epic.

Almost needless to say, things are outdated all over the place. Python is still on version 2.7, and the servers are running on outdated hardware with Debian 8 and 9. The sysadmin left around 2019, and little to no infrastructure maintenance has been done since then.

VPN access no longer works due to outdated software and certificates, making deployments challenging. A typical deployment currently looks something like this:

`ssh` into a Proxmox VM, `pct enter ***`, `vim <file-to-edit>`, `supervisorctl restart ***`, etc.

Besides that, the servers and RAID arrays are quite literally reaching the end of their lives. Some of the drives in the RAID arrays have accumulated more than **13 years of spinning time**.

The main server itself currently has an uptime of **839 days**, and with hardware this old, even a routine reboot would be something of an adventure: there is no guarantee that every disk-or, for that matter, every piece of hardware-will come back up afterwards ;)

The "backup" was maintained by the aforementioned sysadmin. As far as we know, it roughly consists of an `rsync` to a Synology NAS. Nobody knows whether it is still running, whether the backup is complete, or what would happen in the event of a corrupted RAID or disk failure.

In case of a failure, it is unclear whether we could restore the platform to a working state at all. It would certainly require a significant amount of time and effort.

The question is therefore not **if** a failure will happen, but **when**.

Nevertheless, the platform continues to be used daily by the radio [editorial team](https://openbroadcast.ch/discover/editors/) to produce content for the now rather widely distributed [open broadcast radio](https://openbroadcast.ch/) ;)


### Plan (as of 2026)

T.B.D.

## Development Setup

### System

```text
# /etc/hosts
...

# opb - dev
127.0.0.1       obp-next.local
::1             obp-next.local

...
```

```text
# ~/.ssh/config
...

Host obp-lw
    HostName 37.48.80.2
    User root

...
```

#### Binaries

```text
# needed binaries (also see / set .env.example)

ffprobe
ffmpeg
lame

# set to /usr/bin/whoami or similar if no need to test fingerprinting
echoprint-codegen
```

#### Tooling

```text
# needed tooling (see Makefile)
docker
docker-compose
make
uv
bun
```

### Backing Services

See `devsupport/`

```shell
cd devsupport

docker compose build
docker compose up
```

### Project

```shell
make setup
```

### Database

```shell
# list current backups
ssh obp-lw 'ls -lht /nas/backup/db/daily/org_openbroadcast/'

# copy
latest=$(ssh obp-lw 'ls -1t /nas/backup/db/daily/org_openbroadcast/*.sql.gz | head -n1')
rsync "obp-lw:$latest" data/db/dump.sql.gz

# load (takes a while)
gunzip -c data/db/dump.sql.gz \
  | docker compose -f devsupport/compose.yml exec -T mariadb \
      mariadb -uroot -proot obp
```

### Run

NOTE: Separate terminals or whatever you like to run the following commands in parallel.

```shell
make run-be

make run-fe

make run-celery
```

## Post Setup

```shell
# initialize search indexes
./obp-cli search_index --create
```

```shell
# populate some data (feeel free to kill the process after some batches)
./obp-cli search_index --populate --models alibrary.release
./obp-cli search_index --populate --models alibrary.playlist

./obp-cli search_index --populate --models profiles.profile
```

```shell
./obp-cli run
```

## Commands

Some possibly useful commands for development.

```shell
celery -A config worker -B -c 1 -Q celery -n queue.import -l INFO
```


