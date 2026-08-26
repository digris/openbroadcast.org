FROM python:3.7-alpine3.9


# Build toolchain
RUN apk add --no-cache --virtual .build-deps \
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
    automake

# Runtime libs
RUN apk add --no-cache --virtual .run-deps \
    bash \
    libpng \
    libpng-static \
    libmad \
    libid3tag \
    libsndfile \
    gd \
    ffmpeg \
    pcre-dev

# Build FLAC
RUN mkdir -p /src/flac
WORKDIR /src

RUN curl -L \
    "https://codeload.github.com/xiph/flac/tar.gz/1.3.3" \
    -o "flac-1.3.3.tgz"

RUN tar zxf flac-1.3.3.tgz

WORKDIR /src/flac-1.3.3

RUN ./autogen.sh
RUN ./configure --enable-shared=no
RUN make
RUN make install

# Build audiowaveform
WORKDIR /src

RUN curl -L \
    "https://codeload.github.com/bbc/audiowaveform/tar.gz/1.4.2" \
    -o "audiowaveform-1.4.2.tgz"

RUN tar xzf audiowaveform-1.4.2.tgz

WORKDIR /src/audiowaveform-1.4.2

RUN mkdir build

WORKDIR /src/audiowaveform-1.4.2/build

RUN cmake \
    -D ENABLE_TESTS=0 \
    -D BUILD_STATIC=1 \
    ..

RUN make
RUN make install

RUN /usr/local/bin/audiowaveform --version

# Python dependencies
WORKDIR /

COPY services/waveform/requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

# Cleanup only after everything builds
RUN rm -rf /src
RUN apk del .build-deps

RUN /usr/local/bin/audiowaveform --version

# App
RUN mkdir /app/
WORKDIR /app

ADD ./services/waveform/ /app/

EXPOSE 8000

CMD uwsgi --master \
    --pidfile=/tmp/uwsgi.pid \
    --processes 4 \
    --http 0.0.0.0:8000 \
    -w api.wsgi:app