from flask_celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_migrate import Migrate


db = SQLAlchemy(
    session_options={"autoflush": False, "autocommit": False})
redis_store = FlaskRedis()
celery = Celery()
# migrate = Migrate(compare_type=True)
migrate = Migrate()


import pymysql

from api.config import load_config
config = load_config()
testuser = config.testMYSQL_USER
testpassword = config.testMYSQL_PASSWORD
testdatabase = config.testMYSQL_DATABASE
testhost = config.testMYSQL_HOST
testport = config.testMYSQL_PORT

# JOY_USER_user = config.JOY_USER_MYSQL_USER
# JOY_USER_password = config.JOY_USER_MYSQL_PASSWORD
# JOY_USER_database = config.JOY_USER_MYSQL_DATABASE
# JOY_USER_host = config.JOY_USER_MYSQL_HOST
# JOY_USER_port = config.JOY_USER_MYSQL_PORT

#    打开数据库连接
testdb = pymysql.connect(host=testhost, port=testport, user=testuser, password=testpassword, db=testdatabase)
# joyuser_db = pymysql.connect(host=JOY_USER_host, port=JOY_USER_port, user=JOY_USER_user, password=JOY_USER_password, db=JOY_USER_database)

