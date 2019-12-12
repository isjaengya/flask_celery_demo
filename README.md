# flask_celery_demo

#### 启动flask项目
```python
一般都是用gunicorn启动flask
gunicorn -c api/config/gunicorn.py -b 0.0.0.0:8001 wsgi:application
```

#### 启动celery
```python
在项目根目录下(即执行启动flask命令的下面执行)
celery -A celery_worker.celery worker  # 这个命令只是让你测试好测试，如果有定时任务还是要还是要分为master和worker
```
