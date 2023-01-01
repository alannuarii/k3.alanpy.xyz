from multiprocessing import cpu_count
from os import environ

def max_workers():
    return cpu_count()

chdir = '/home/alanwebi/repositories/k3app.alanpy.xyz/flask_app'
bind = '127.0.0.1:52782'
max_requests = 100
workers = 1
worker_class = 'tornado'
errorlog = 'error.log'
loglevel = 'error'
wsgi_app = 'wsgi:app'
pidfile = 'gunicorn.pid'
pythonpath = '/home/alanwebi/.asdf/shims/python'
daemon = True
