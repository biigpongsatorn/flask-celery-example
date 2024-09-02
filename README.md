# Flask-Celery-Example

### Run celery
```sh
celery -A app.celery worker --concurrency=3 --loglevel INFO
```

### Run Flask
```
python app.py
```

### Test
```
curl -X POST http://localhost:8999/api/long_task

curl http://localhost:8999/api/task_status/<task_id>
```