# Audio Waveform Generator


TODO: refactor to Quart and run on GCP / Cloud Run.

## Development - Service

run in flask app (local)
NOTE: needs ffprobe, ffmpeg & audiowaveform binaries

```shell
uwsgi --http 0.0.0.0:8099 -w api.wsgi:app
```

run in uwsgi mode (local)

```shell
uwsgi --http 0.0.0.0:8099 -w api.wsgi:app
```

build docker image (Service)

```shell
docker build -t waveform-service:latest .
```


run as docker container

```shell
docker run --rm -p 5000:8000 waveform-service:latest
```


### Deploy to OBP docker host

(Also see `Makefile`)

```shell
docker build -t waveform-service:latest .

docker save waveform-service:latest | \
  ssh -C 10.10.8.202 docker load
```

```shell
# on docker host
docker stop waveform-service
docker rm waveform-service
docker run -d -p 2001:8000 --name waveform-service --restart unless-stopped waveform-service:latest
```

