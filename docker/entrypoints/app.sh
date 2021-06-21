#!/usr/bin/env bash

exec ./wait-for.sh ${POSTGRES_HOST}:${POSTGRES_PORT} -- "$@"
