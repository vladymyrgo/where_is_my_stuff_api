from ..celery import app

from .utils.send_mail import send_mail_alternatives


@app.task
def task_send_mail(*args, **kwargs):
    send_mail_alternatives(*args, **kwargs)
