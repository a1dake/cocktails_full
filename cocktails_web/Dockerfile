FROM node:16.18-alpine3.16

WORKDIR /frontend_build

COPY package.json .
COPY package-lock.json .

RUN apk update && \
    apk add bash && \
    npm install && \
    npm cache rm --force

WORKDIR /frontend

COPY . .

RUN chmod 0700 entrypoint.sh

EXPOSE 8080

CMD [ "bash", "entrypoint.sh" ]

