FROM webdevops/liquibase:postgres

RUN apt-get update && apt-get install -y --no-install-recommends netcat \
    && rm -rf /var/lib/apt/lists/*

COPY docker/entrypoints/migrator.sh docker/wait-for.sh ./

WORKDIR changelog

COPY src/api/infrastructure/models/changelog .

ENTRYPOINT ["/liquibase/migrator.sh"]

CMD ["update"]
