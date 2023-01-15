#!/bin/sh
set -e

# Start Nginx
nginx -c /app/deploy/nginx.conf

# Start uWSGI
uwsgi --ini deploy/uwsgi.ini