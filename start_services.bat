@echo off

@REM start /b celery -A Home worker --loglevel=info
start /b celery -A Home worker --pool=eventlet -l debug

@REM echo "test1"
timeout /t 10
@REM echo "test2"

celery -A Home call CeleryTasks.tasks.listen_to_blockchain_task
@REM python -c "from CeleryTasks.tasks import listen_to_blockchain_task; listen_to_blockchain_task.delay()"

@REM echo "test3"

daphne Home.asgi:application -b 0.0.0.0 -p 8000