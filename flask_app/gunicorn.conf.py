from multiprocessing import cpu_count
from os import environ

def max_workers():
    return cpu_count()

chdir = '/home/alanwebi/repositories/K3App/flask_app'
bind = '127.0.0.1:52335'
max_requests = 1000
workers = max_workers()
worker_class = 'tornado'
errorlog = 'error.log'
loglevel = 'error'
wsgi_app = 'wsgi:app'
pidfile = 'gunicorn.pid'
pythonpath = '/home/alanwebi/.asdf/shims/python'
daemon = True
