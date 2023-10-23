@echo off

@REM start /b celery -A Home worker --loglevel=info
start /b celery -A Home worker --pool=eventlet -l debug

timeout /t 10

celery -A Home call CeleryTasks.tasks.listen_to_blockchain_task

daphne Home.asgi:application -b 0.0.0.0 -p 8000