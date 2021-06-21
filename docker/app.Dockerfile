FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1

ARG APP_USER=picture_uploader
ARG INSTALL_DEV_DEPENDENCIES=false

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # gcc required for dependency-injector
    gcc \
    libc6-dev \
    netcat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m $APP_USER
USER $APP_USER
RUN mkdir -p /home/$APP_USER/app
WORKDIR /home/$APP_USER/app
ENV PATH="/home/${APP_USER}/.local/bin:$PATH"

RUN mkdir -p media/files/

RUN pip install --user --no-cache poetry

COPY src/requirements .

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root \
    $(test $INSTALL_DEV_DEPENDENCIES = "false" && echo "--no-dev")

COPY --chown=$APP_USER src .
COPY --chown=$APP_USER ./docker/wait-for.sh ./docker/entrypoints/app.sh ./

ENTRYPOINT ["./app.sh"]

CMD ["gunicorn", "-c", "api/gunicorn.conf.py", "api.wsgi:app"]
