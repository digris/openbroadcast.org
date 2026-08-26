FROM python:3.7-alpine3.9

ADD requirements.txt /requirements.txt

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
        git \
        curl \
        make \
        cmake \
        gcc \
        g++ \
        libmad-dev \
        libid3tag-dev \
        libsndfile-dev \
        boost-dev \
        boost-static \
        gd-dev \
        zlib-dev \
        libpng-dev \
        libtool \
        gettext \
        autoconf \
        automake \
    && apk add --no-cache --virtual .run-deps \
        bash \
        libpng \
        libpng-static \
        libmad \
        libid3tag \
        libsndfile \
        gd \
        ffmpeg \
        pcre-dev \
    && mkdir /src \
    && cd /src \
    && curl -L "https://codeload.github.com/xiph/flac/tar.gz/1.3.3" -o "flac-1.3.3.tgz" \
    && tar zxf flac-1.3.3.tgz \
    && cd flac-1.3.3 \
    && ./autogen.sh \
    && ./configure --enable-shared=no \
    && make \
    && make install \
    && cd /src \
    && curl -L "https://codeload.github.com/bbc/audiowaveform/tar.gz/1.4.2" -o "audiowaveform-1.4.2.tgz" \
    && tar xzf audiowaveform-1.4.2.tgz \
    && cd audiowaveform-1.4.2 \
    && mkdir build \
    && cd build \
    && cmake -D ENABLE_TESTS=0 -D BUILD_STATIC=1 .. \
    && make \
    && make install \
    && cd /src \
    && pip3 install -r /requirements.txt \
    && cd / \
    && rm -R /src \
    && apk del .build-deps \
    && /usr/local/bin/audiowaveform --version

RUN /usr/local/bin/audiowaveform --version

RUN mkdir /app/
WORKDIR /app

ADD . /app/

EXPOSE 8000
CMD uwsgi --master --pidfile=/tmp/uwsgi.pid --processes 4 --http 0.0.0.0:8000 -w api.wsgi:app
