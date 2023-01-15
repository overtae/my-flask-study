FROM python:3.10-alpine

COPY . /app
WORKDIR /app

RUN apk update && \
    apk add \
            nginx \
            build-base \
            linux-headers 

RUN pip3 install --upgrade pip && \
    pip install -r requirements.txt

RUN chmod +x /app/deploy/entrypoint.sh
ENTRYPOINT [ "/app/deploy/entrypoint.sh" ]