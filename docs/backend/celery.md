# Celery

Redis is used as broker

## Run celery worker
- `celery worker -A rs_exchange -B` - run celery worker for all queues
- `celery worker -A rs_exchange -Q my_queue` - run celery worker for specific queue

## Queues
- add new queue in settings: CELERY_QUEUES
- use `@app.task` decorator for default queue or `@app.task(queue='my_queue')` to specify queue
