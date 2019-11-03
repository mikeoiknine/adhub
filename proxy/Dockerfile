FROM nginx:alpine
 
COPY nginx.conf /etc/nginx/nginx.conf

RUN apk update && apk add bash

EXPOSE 80/tcp
EXPOSE 443/tcp

CMD ["/bin/sh", "-c", "exec nginx -g 'daemon off;';"]