from .celery import celery_app


@celery_app.task
def send_notifications():
    print('Sending notifications...')
    # Code to send notifications
    print('Notifications sent!')
