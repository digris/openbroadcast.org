# Devsupport

The whole dev stack runs in docker compose. Single entry point:

    http://obp-next.local:5000

(`/etc/hosts`: `127.0.0.1 obp-next.local` - `localhost:5000` works as well, but
the socket.io url is fixed to `obp-next.local`, see `PUSHY_SOCKET_SERVER`.)

## Usage

From the project root (see `Makefile`):

```shell
make up      # build & start (detached)
make logs    # follow logs
make ps
make down
make cli ARGS="search_index --create"   # ./obp-cli (manage.py) in the core container
```

Optional: `cp devsupport/.env.example devsupport/.env` for secrets passed to `core`.

## Layout

| service         | what                                    | host port   |
| --------------- | --------------------------------------- | ----------- |
| `proxy`         | caddy, the only http entry point        | 5000        |
| `core`          | django `runserver` + celery worker/beat | -           |
| `ui`            | webpack-dev-server (bundle + hmr)       | -           |
| `pushy`         | socket.io gateway (redis pub/sub)       | 5001        |
| `waveform`      | waveform service                        | 5002        |
| `mariadb`       | database                                | 3307        |
| `rabbitmq`      | celery / playout broker                 | 5672, 15672 |
| `redis`         | pushy pub/sub                           | 6379        |
| `elasticsearch` | search (amd64 image, emulated on arm)   | 9200        |

Routing (`proxy/Caddyfile`):

- `/socket.io/*` -> `pushy`
- `/sockjs-node/*`, `/static/js/*` -> `ui`. Paths under `/static/js/` that are
  not part of the bundle fall through to `core` (`devServer.proxy`).
- everything else -> `core`, with the `X-WEBPACK-DEVSERVER` header set (templates
  then load the dev bundle, see `obp_core/legacy_apps/webpack`).

## Code mounts & reload (`compose.override.yml`)

- `core`: `obp_core/` and `config/` are mounted - `runserver` reloads on change.
  Celery does **not** reload: restart `core` after changing task code.
- `ui`: `obp_ui/` and `webpack.config.js` are mounted - webpack recompiles / hmr
  (polling, `WEBPACK_WATCH_POLL`). A changed `webpack.config.js` needs a restart of `ui`.
- changed dependencies (`pyproject.toml` / `uv.lock`, `package.json` / `bun.lock`):
  `make up` rebuilds the images.
- `data/` is mounted into `core` at `/app/data` (media files).

## Images

- `core/Dockerfile`: `python:3.9-slim` + build toolchain (the legacy pins have no
  linux wheels), `ffmpeg`, `lame`. `echoprint-codegen` is the mock from `bin/`.
  Runs as root with `C_FORCE_ROOT` (celery + pickle) - dev only.
- `ui/Dockerfile`: `node:22-slim` + `bun` (package manager only - webpack 4 runs on node).

## Settings / environment

In-network hosts are passed via environment (`compose.yml`), the defaults in
`config/settings/` still point at the published ports on `127.0.0.1`:
`DATABASE_URL`, `CELERY_BROKER_URL`, `PLAYOUT_BROKER_URL`, `ELASTICSEARCH_URL`,
`WAVEFORM_SERVICE_ENDPOINT`, `PUSHY_REDIS_HOST`, `PUSHY_SOCKET_SERVER`.

Webpack: `WEBPACK_PUBLIC_PATH`, `WEBPACK_SOCK_PORT`, `WEBPACK_PROXY_TARGET`,
`WEBPACK_WATCH_POLL` (`webpack.config.js`).

## Notes / open ends

- the compose project name is `obp` (`name:` in `compose.yml`): containers are
  `obp-<service>-1`, volumes `obp_obp-mariadb` / `obp_obp-elasticsearch`.
- no automatic `migrate` on start: the database comes from a dump (see root README).
- `nginx/` is not used anymore (replaced by `proxy/`).
- `obp_core/search/duplicate_detection.py` has a hardcoded `localhost:9200`.
- tests / lint still run on the host (`make test`, `make lint`).
