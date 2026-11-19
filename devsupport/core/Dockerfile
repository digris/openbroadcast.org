FROM python:3.9-slim

WORKDIR /app/

ENV PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_VERSION=0.8.14 \
    UV_FROZEN=1

# NOTE: build toolchain & headers are needed for the legacy pins without
#       (linux / arm64) wheels: Pillow, uWSGI, python-Levenshtein, ...
RUN set -ex \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        tini \
        build-essential \
        dpkg-dev \
        libjpeg-dev \
        zlib1g-dev \
        libfreetype6-dev \
        libmagic1 \
        libmagickwand-dev \
        ffmpeg \
        lame \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir --timeout 60 "uv==$UV_VERSION"

COPY \
  pyproject.toml \
  uv.lock \
  ./

# local path dependencies of pyproject.toml (see [tool.uv.sources])
COPY pip-legacy-packages/ ./pip-legacy-packages/

# NOTE: the dev image includes the dev dependency group - tests run in the container
RUN uv sync --no-install-project

COPY config/ ./config/
COPY obp_core/ ./obp_core/
# un-bundled ui assets, served by django (STATICFILES_DIRS: build/static)
COPY obp_ui/font/ ./build/static/font/
COPY obp_ui/img/ ./build/static/img/
COPY obp_ui/icons/ ./build/static/icons/
COPY devsupport/bin/mock-echoprint-codegen.py /usr/local/bin/echoprint-codegen
COPY devsupport/core/start.sh manage.py cli ./

ENV PATH="/app/.venv/bin:$PATH"

# NOTE: C_FORCE_ROOT - celery refuses to run as root with pickle serialization.
#       acceptable for the dev container only.
ENV DJANGO_SETTINGS_MODULE=config.settings.dev \
    C_FORCE_ROOT=1 \
    PORT=5000

EXPOSE 5000

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["./start.sh"]
