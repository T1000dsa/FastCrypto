from celery import Celery


celery = Celery(
    'crypto_updater',
    broker='redis://localhost:6379/0',  # Redis as broker
    backend='redis://localhost:6379/1'  # Store task results
)