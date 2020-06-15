FROM postgres
COPY ./docker/init.sql /docker-entrypoint-initdb.d/