from celery.schedules import crontab
from kombu import (Queue, Exchange)

# from api.config.default import DefaultConfig


class ProductionConfig():

    DEBUG = False

