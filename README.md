# open broadcast - platform

[![Actions Status](https://github.com/digris/openbroadcast.org/workflows/CD/badge.svg)](https://github.com/digris/openbroadcast.org/actions)


## Development Installation

```shell

```


### Tooling

#### Ptyhon

```shell
pyenv install 2.7.18
pyenv local 2.7.18

poetry env use python2.7
poetry install
```


#### Node

```shell
nvm use v14
```


### Dependencies

#### System Libraries & Utilities

```shell
# dfn
# utilities
sudo dnf install \
  lame \
  sox \
  faad2 \
  ffmpeg

# libraries
sudo dnf install \
  libsndfile \
  libsndfile-devel
```

```shell
pip install numpy==1.8.0
pip install MySQL-python==1.2.5
pip install -r requirements.txt

yarn install
```


### Backing Services

Backing services can be run using `docker-compose`:

```shell
docker-compose up --build
```


## Release

```shell
# requirements
poetry export \
  -f requirements.txt \
  --output requirements.txt

# build assets
yarn dist
```
