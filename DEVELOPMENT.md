# Development

## Project Setuo

### Backing Services

See `devsupport/`

```shell
cd devsupport

docker compose build
docker compose up
```

### Project

```shell

```



## Post Setuo

```shell
./obp-cli search_index --create
```

```shell
# search indexes
./obp-cli search_index --populate --models alibrary.playlist
```

```shell
./obp-cli run
```

```shell
celery -A config worker -B -c 1 -Q celery -n queue.import -l INFO
```