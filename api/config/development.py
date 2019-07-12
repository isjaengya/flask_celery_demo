from celery.schedules import crontab
from kombu import (Queue, Exchange)

from api.config.default import DefaultConfig


class DevelopmentConfig(DefaultConfig):
    DEBUG = True

    SIGNATURE = True

    # SQL
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_PORT = '3306'
    MYSQL_DATABASE = 'yinyu_dev'
    MYSQL_HOST = '127.0.0.1'

    SQLALCHEMY_DATABASE_URI = \
        "mysql://{}:{}@{}:{}/{}".format(
            MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = ''

    # JOYUSER SQL
    testMYSQL_USER = 'root'
    testMYSQL_PASSWORD = 'root'
    testMYSQL_PORT = 3306
    testMYSQL_DATABASE = 'yinyu_dev'
    testMYSQL_HOST = '127.0.0.1'

    USER_URL = 'http://.com/user}'
    ACTIVITY_JOIN_URL = 'https://.cin'
    BADGE_GAIN_URL = 'http://com/b'
    CHECK_SESSION = 'http://.com/s}'

    UPLOAD_CDN_URL = 'https://.com/moad'

    CELERY_BROKER_URL = 'redis://:{}@{}:6379/10'.format(REDIS_PASSWORD, REDIS_HOST)
    # CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
    # CELERY_DEFAULT_QUEUE = 'default'
    # CELERY_ENABLE_UTC = False
    # CELERY_IMPORTS = (
    #     'tasks.celery_demo',
    # )
    #
    # CELERY_QUEUES = {
    #     Queue('default', Exchange('default'), routing_key='default'),
    #     Queue('demo', Exchange('demo'), routing_key='demo'),
    #
    # }
    #
    # CELERY_ROUTES = {
    #     'tasks.celery_demo.*': {'queue': 'default', 'routing_key': 'default'},
    #     'tasks.celery_demo': {'queue': 'demo', 'routing_key': 'demo'},
    # }
#