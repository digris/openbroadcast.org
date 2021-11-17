# open broadcast - platform

[![Actions Status](https://github.com/digris/openbroadcast.org/workflows/CD/badge.svg)](https://github.com/digris/openbroadcast.org/actions)


## Development Installation

```shell
cd ~/code
git clone git@github.com:digris/openbroadcast.org.git openbroadcast.org
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

yarn install
```


### Backing Services

Backing services can be run using `docker-compose`:

```shell
docker-compose -f ./docker/docker-compose.yml up --build
```


## Build Release

```shell
# requirements
poetry export \
  -f requirements.txt \
  --output requirements.txt

# build assets
yarn dist
```

```shell
# or via make
make build
```


## Deploy

Deployment is handled via ansible: [obp-infrastructure](https://github.com/digris/obp-infrastructure)

```shell
cd obp-infrastructure/ansible
./deploy.sh
```
