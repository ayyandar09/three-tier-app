# Stage 1: Build the React application
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build


# Stage 2: Serve with Nginx
FROM nginx:alpine

RUN apk update && apk upgrade

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Prepare Nginx for non-root execution
RUN mkdir -p /var/cache/nginx \
    /var/run/nginx \
    /tmp/nginx \
    /tmp/client_temp \
    /tmp/proxy_temp \
    /tmp/fastcgi_temp \
    /tmp/uwsgi_temp \
    /tmp/scgi_temp \
    && chown -R 101:101 /var/cache/nginx \
    /var/run/nginx \
    /usr/share/nginx/html \
    /tmp/nginx \
    /tmp/client_temp \
    /tmp/proxy_temp \
    /tmp/fastcgi_temp \
    /tmp/uwsgi_temp \
    /tmp/scgi_temp

# Change Nginx to non-root port
RUN sed -i 's/listen       80;/listen       8080;/' \
    /etc/nginx/conf.d/default.conf \
    && sed -i 's@pid        /run/nginx.pid;@pid        /tmp/nginx/nginx.pid;@' \
    /etc/nginx/nginx.conf

USER 101

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]