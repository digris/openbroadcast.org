FROM node:14-slim

WORKDIR /root/

ADD ./services/pushy/package.json .
ADD ./services/pushy/package-lock.json .
ADD ./services/pushy/pushy.js .

RUN yarn install

ADD ./docker/pushy/config.json .


CMD ["node", "pushy.js"]
