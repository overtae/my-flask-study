FROM node:18-alpine

COPY . /app
WORKDIR /app

RUN npm install

RUN npm ci --only=production

RUN apk update && \
    apk add nginx

RUN chmod +x /app/deploy/entrypoint.sh

ENTRYPOINT [ "/app/deploy/entrypoint.sh" ]