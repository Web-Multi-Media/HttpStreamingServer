FROM nginx:1.15.0-alpine

RUN apk add --no-cache apache2-utils

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
