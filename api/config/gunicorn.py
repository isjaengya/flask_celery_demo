import multiprocessing

# 监听本机的5000端口
bind = '0.0.0.0:5000'

preload_app = True

# 开启进程
workers = multiprocessing.cpu_count() * 2 + 1

# 每个进程的开启线程
threads = multiprocessing.cpu_count() * 2

backlog = 2048

# 工作模式为meinheld
worker_class = "egg:meinheld#gunicorn_worker"

# debug=True

# 如果不使用supervisord之类的进程管理工具可以是进程成为守护进程，否则会出问题
daemon = False

# 进程名称
proc_name = 'gunicorn.pid'

# 进程pid记录文件
pidfile = 'app_pid.log'

loglevel = 'debug'
logfile = 'debug.log'
accesslog = 'access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(D)s %(f)s %(a)s'
