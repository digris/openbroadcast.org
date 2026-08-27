# Open Broadcast - Platform

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