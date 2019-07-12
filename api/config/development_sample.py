from celery.schedules import crontab
from kombu import (Queue, Exchange)

from api.config.default import DefaultConfig


class DevelopmentConfig(DefaultConfig):

    DEBUG = True

    # SQL
    MYSQL_USER = ''
    MYSQL_PASSWORD = ''
    MYSQL_PORT = ''
    MYSQL_DATABASE = ''
    MYSQL_HOST = ''

    # redis
    REDIS_HOST = ''
    REDIS_PORT = 6379
    REDIS_DB = 0
    PASSWORD = ''

    # cache redis
    CACHE_REDIS_HOST = 'redis'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_PASSWORD = ''

    # api redis
    API_REDIS_HOST = 'redis'
    API_REDIS_PORT = 6379
    API_REDIS_DB = 0
    API_PASSWORD = ''

    # sensors
    PROJECT_HOME = ''
    SENSORS_PROJECT_NAME = 'yinyu_test'
    SENSOR_URL = ''
    SENSOR_TOKEN = ''

    # celery
    CELERY_ENABLE_UTC = False
    CELERY_TASK_RESULT_EXPIRES = 86400
    CELERY_IMPORTS = (
        "tasks.timing"
    )

    CELERY_BROKER_URL = 'redis://:{}@{}:9379/10'.format(PASSWORD, REDIS_HOST)
    CELERYBEAT_SCHEDULE = {
        'test': {
            'task': 'test',
            'schedule': crontab(minute=3),
            'options': {
                'queue': 'timing'
            }
        },
    }
    CELERY_QUEUES = {
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('timing', Exchange('timing'), routing_key='timing'),

    }
    CELERY_DEFAULT_QUEUE = 'default'
    CELERY_SEND_EVENTS = True
    CELERY_TASK_IGNORE_RESULT = True
    CELERYD_MAX_TASKS_PER_CHILD = 50

    # api
    API_DOMAIN = ''
    API_ROOMS_CARDS_URL = ''

    # impala
    IMPALA_HOST = 'node02.sixkb.sa'
    IMPALA_PORT = 21050
    IMPALA_DATABASE = 'rawdata'

    # nginx file
    NGINX_DOWNLOAD_UC_FILE = ''
    NGINX_DOWNLOAD_UC_MD5 = ''
    NGINX_DOWNLOAD_C_FILE = ''
    NGINX_DOWNLOAD_C_MD5 = ''
    NGINX_DOWNLOAD_RC_FILE = ''
    NGINX_DOWNLOAD_RC_MD5 = ''
    NGINX_DOWNLOAD_VS3_C_FILE = ''
    NGINX_DOWNLOAD_VS3_C_MD5 = ''
    NGINX_DOWNLOAD_RC_V2_FILE = ''
    NGINX_DOWNLOAD_RC_V2_MD5 = ''
    NGINX_DOWNLOAD_C_RELATION_FILE = ''
    NGINX_DOWNLOAD_UC_VIDEO_FILE = ''
    NGINX_DOWNLOAD_UC_VIDEO_MD5 = ''
    NGINX_DOWNLOAD_UC_VIDEO_TMP = ''
    NGINX_DOWNLOAD_COLD_BOOT_FILE = ''
    NGINX_DOWNLOAD_COLD_BOOT_DIR = ''
    NGINX_DOWNLOAD_MANUAL_FILE = ''
    NGINX_DOWNLOAD_MANUAL_MD5 = ''

    # email
    MAIL_HOST = '.com'
    MAIL_USER = '.cn'
    MAIL_PASSWORD = ''
    SENDER = '.cn'
    EMAIL_FILE_PATH = ''
