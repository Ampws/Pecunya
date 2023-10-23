#!/bin/bash

start_celery() {
    celery -A Home worker --loglevel=info &
}

start_django() {
    daphne Home.asgi:application -b 0.0.0.0 -p 8000
}

start_celery
start_django
