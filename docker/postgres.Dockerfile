FROM postgres:12.5-alpine

WORKDIR /docker-entrypoint-initdb.d
COPY ./docker/entrypoints/init-db.sh .

