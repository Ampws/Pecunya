@echo off

REM Start the Celery worker
start /b celery -A Pecunya worker --loglevel=info

REM Start the Daphne server
daphne Home.asgi:application -b 0.0.0.0 -p 8000
