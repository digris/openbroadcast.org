Edge Server(s)
#############


Main Webserver
*********************

 - node01



Nginx
=====

.. code-block:: bash

    aptitude install nginx


.. code-block:: bash

    /etc/nginx/sites-enabled/stage.openbroadcast.org.conf


nginx config (comes from repository!):
::::::::::::::::::::::::::::::::::::::


.. code-block:: bash

    limit_req_zone $binary_remote_addr zone=daysy:10m rate=5r/s;
    limit_req_zone $binary_remote_addr zone=daysy_static:10m rate=20r/s;
    limit_req_zone $binary_remote_addr zone=daysy_api:10m rate=10r/s;

    server {

        listen 80;
        server_name stage.openbroadcast.org;
        access_log  /var/log/nginx/stage.openbroadcast.org;

        gzip  on;
        gzip_comp_level 2;
        gzip_proxied any;
        gzip_types text/plain text/css application/x-javascript text/xml application/xml application/xml+rss text/javascript text/json;


        sendfile        on;
        client_max_body_size 1024M;


        location /static  {
            limit_req zone=daysy_static burst=120 nodelay;
            autoindex  off;
            root /nas/storage/stage.openbroadcast.org/;
            expires 30d;
            add_header Pragma public;
            add_header Cache-Control "public";
        }

        location /media  {
            limit_req zone=daysy_static burst=120 nodelay;
            autoindex  off;
            root /nas/storage/stage.openbroadcast.org/;
            expires 30d;
            add_header Pragma public;
            add_header Cache-Control "public";
        }

        location / {

            limit_req zone=daysy burst=10 nodelay;

            proxy_pass http://172.20.10.204:8011; # the stage backend
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }


Node.js - pushy websocket server
================================

.. code-block:: bash

    aptitude install git-core curl build-essential openssl libssl-dev



.. code-block:: bash

    cd ~/src/
    wget http://nodejs.org/dist/v0.10.26/node-v0.10.26.tar.gz
    tar xzfv node-v0.10.26.tar.gz
    cd node-v0.10.26
    ls
    ./configure
    make
    make install


.. code-block:: bash

cd /srv/
mkdir pushy.stage.openbroadcast.org
cd pushy.stage.openbroadcast.org/
git clone https://github.com/ohrstrom/django-pushy.git
cd server/
npm install

# configure and test
nano config.json
node pushy.js

# supervisor service
nano /etc/supervisor/conf.d/pushy.stage.openbroadcast.org.conf

supervisorctl reread
supervisorctl update
supervisorctl status



supervisor config
:::::::::::::::::

.. code-block:: bash

    [program:pushy.stage.openbroadcast.org]
    directory=/srv/pushy.stage.openbroadcast.org/server
    command=/usr/local/bin/node /srv/pushy.stage.openbroadcast.org/server/pushy.js
    user=root
    autostart=true
    autorestart=true
    redirect_stderr=True
    environment=HOME='/root/'
    stdout_logfile_maxbytes=10MB
    stdout_logfile_backups=5
    stdout_logfile=/var/log/supervisor/pushy.stage.openbroadcast.org




Varnish
=======

.. code-block:: bash

    curl http://repo.varnish-cache.org/debian/GPG-key.txt | apt-key add -
    echo "deb http://repo.varnish-cache.org/debian/ wheezy varnish-3.0" >> /etc/apt/sources.list
    apt-get update
    aptitude install varnish



Varnish quick'n'dirty config
::::::::::::::::::::::::::::



.. code-block:: bash

# 172.20.10.204:8011 is stage

backend default {
    .host = "172.20.10.204";
    .port = "8011";
}

sub vcl_recv {
    # unless sessionid/csrftoken is in the request, don't pass ANY cookies (referral_source, utm, etc)
    if (req.request == "GET" && (req.url ~ "^/static" || (req.http.cookie !~ "sessionid" && req.http.cookie !~ "csrftoken"))) {
        remove req.http.Cookie;
    }

    # normalize accept-encoding to account for different browsers
    # see: https://www.varnish-cache.org/trac/wiki/VCLExampleNormalizeAcceptEncoding
    if (req.http.Accept-Encoding) {
        if (req.http.Accept-Encoding ~ "gzip") {
            set req.http.Accept-Encoding = "gzip";
        } elsif (req.http.Accept-Encoding ~ "deflate") {
            set req.http.Accept-Encoding = "deflate";
        } else {
            # unknown algorithm
            remove req.http.Accept-Encoding;
        }
    }
}

sub vcl_fetch {
    # static files always cached
    if (req.url ~ "^/static") {
       unset beresp.http.set-cookie;
       return (deliver);
    }

    # pass through for anything with a session/csrftoken set
    if (beresp.http.set-cookie ~ "sessionid" || beresp.http.set-cookie ~ "csrftoken") {
       return (hit_for_pass);
    } else {
       return (deliver);
    }
}