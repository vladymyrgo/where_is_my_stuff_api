from django.conf import settings
import celery.bin.celery

from base.utils.send_mail import send_mail_alternatives


def celery_is_running():
    """Check if celery is running and return True or False.
    """
    if settings.CELERY_ALWAYS_EAGER:  # if tests is running without celery daemon
        return True
    else:  # pragma: no cover
        try:
            status = celery.bin.celery.CeleryCommand.commands['status']()
            status.app = status.get_app()
            status.run()
            return True
        except celery.bin.base.Error as e:
            if e.status == celery.platforms.EX_UNAVAILABLE:
                return False
            raise e


def run_task_with_or_without_celery(task, *args, **kwargs):
    """Run task in celery if celery is running and run task not asynchronously
    if celery isn't running. Notify admins by email if celery isn't running.
    """
    if celery_is_running():
        task.delay(*args, **kwargs)
    else:  # pragma: no cover
        # notify admins that celery is not running
        to = [admin[1] for admin in settings.ADMINS]
        subject = 'Problem on server!'
        html_content = '<p>Celery is not running! Please contact developers.</p>'
        send_mail_alternatives(to, subject, html_content)

        # run task not in celery daemon
        task(*args, **kwargs)
