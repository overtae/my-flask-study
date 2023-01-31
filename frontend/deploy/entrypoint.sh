#!/bin/sh
set -e

# Start Nginx
nginx -c /app/deploy/nginx.conf

# Start NodeJS
node server.js