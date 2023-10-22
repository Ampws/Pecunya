@echo off

start /b celery -A Home worker --loglevel=info

@REM echo "test1"
@REM timeout /t 10
@REM echo "test2"

@REM celery -A Home call CeleryTasks.tasks.listen_to_blockchain_task
@REM python -c "from CeleryTasks.tasks import listen_to_blockchain_task; listen_to_blockchain_task.delay()"

@REM echo "test3"

daphne Home.asgi:application -b 0.0.0.0 -p 8000