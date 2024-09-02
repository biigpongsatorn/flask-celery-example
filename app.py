from flask import Flask, jsonify
from celery import Celery

app = Flask(__name__)

# Configure Celery with a broker (e.g., Redis)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6378/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Limiting the max concurrency to 3
celery.conf.update(
    worker_concurrency=3,
    task_default_queue='default',
)


@celery.task()
def long_task():
    # Simulate a long task
    import time
    print('long_task hellooooooooo')
    time.sleep(10)  # Simulates a task that takes 60 seconds
    return True


@app.route('/api/long_task', methods=['POST'])
def send_request():
    print('send_request')
    # Queue the long task
    task = long_task.apply_async()
    return jsonify({'task_id': task.id, 'status': 'Task has been started'}), 202


@app.route('/api/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    # Check the status of the task
    task = long_task.AsyncResult(task_id)
    response = {
        'task_id': task.id,
        'status': task.state,
        'result': task.result if task.state == 'SUCCESS' else None,
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8999, debug=True)
