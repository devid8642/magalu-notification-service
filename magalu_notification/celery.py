from celery import Celery
from decouple import config


celery_app = Celery(
    'magalu_notification',
    broker=config('CELERY_BROKER_URL', default='redis://localhost:6379/0'),
    backend=config('CELERY_BACKEND_URL', default='redis://localhost:6379/1'),
)


celery_app.conf.beat_schedule = {
    'send-notifications': {
        'task': 'magalu_notification.celery_tasks.send_notifications',
        'schedule': 10,
    },
}

celery_app.autodiscover_tasks(['magalu_notification.celery_tasks'])
