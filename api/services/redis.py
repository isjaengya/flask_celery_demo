import redis
from flask import (current_app, has_app_context)


if has_app_context():
    print('have flask context')
    host = current_app.config.get('REDIS_HOST')
    port = current_app.config.get('REDIS_PORT')
    db = current_app.config.get('REDIS_DB')
    password = current_app.config.get('REDIS_PASSWORD')

    # cache_host = current_app.config.get('CACHE_REDIS_HOST')
    # cache_port = current_app.config.get('CACHE_REDIS_PORT')
    # cache_db = current_app.config.get('CACHE_REDIS_DB')
    # cache_password = current_app.config.get('CACHE_PASSWORD')

else:
    print('no flask context')
    from api.config import load_config
    config = load_config()
    host = config.REDIS_HOST
    port = config.REDIS_PORT
    db = config.REDIS_DB
    password = config.REDIS_PASSWORD

    # cache_host = config.CACHE_REDIS_HOST
    # cache_port = config.CACHE_REDIS_PORT
    # cache_db = config.CACHE_REDIS_DB
    # cache_password = config.CACHE_PASSWORD

if password:
    pool = redis.ConnectionPool(host=host, port=port, db=db, password=password, decode_responses=True)
    # cache_pool = redis.ConnectionPool(host=cache_host, port=cache_port, db=cache_db, password=cache_password, decode_responses=True)
else:
    pool = redis.ConnectionPool(host=host, port=port, db=db, decode_responses=True)
    # cache_pool = redis.ConnectionPool(host=cache_host, port=cache_port, db=cache_db, decode_responses=True)


redis_client = redis.Redis(connection_pool=pool)
# cache_redis_client = redis.Redis(connection_pool=cache_pool)
