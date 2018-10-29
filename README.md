# Open Broadcast - Platform


## Run Development

    # web application
    ./manage.py runserver 0.0.0.0:8080
    
    # tasks
    celery -A project worker -c 1 -Q celery,process,import,complete,grapher,convert,index -l debug

    # webpack devserver
    npm run watch

    # websocket
    cd ~/code/openbroadcast/pushy/server/ && node pushy.js

    # elasticsearch
    ~/.dotfiles/bin/elasticsearch -Ehttp.port=9200
