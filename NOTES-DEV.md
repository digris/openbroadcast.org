# DEV Install - 2025-07-09

```shell
cd ~/code
git clone git@github.com:digris/openbroadcast.org.git openbroadcast.org
```

## Backing Services

see `docker/docker-compose.yml`

```shell
docker compose -f docker/docker-compose.yml up -d
```

## Python

```shell
pyenv install 2.7.18
```

```shell
~/.pyenv/versions/2.7.18/bin/pip \
  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host  files.pythonhosted.org \
  install poetry

~/.pyenv/versions/2.7.18/bin/poetry --version
# 1.1.15
```

```shell
~/.pyenv/versions/2.7.18/bin/poetry install
```

```shell
# activate virtualenv
~/.pyenv/versions/2.7.18/bin/poetry shell
```

```shell
nvm install v20
nvm use 20
nvm install yarn
yarn install
```


```shell
brew install \
  libmagic \
  imagemagick \
  lame \
  sox \
  faad2 \
  ffmpeg
```



## Post Install

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