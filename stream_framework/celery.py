from __future__ import absolute_import
import stream_framework.verbs.base
#import os

## Broker settings.
#BROKER_URL = 'redis://localhost:6379'
#BROKER_URL = 'redis://192.168.99.100:32770'

# List of modules to import when celery starts.
#CELERY_IMPORTS = ('myapp.tasks', )

## Using the database to store task state and results.
#CELERY_RESULT_BACKEND = 'redis://localhost:6379'
#CELERY_RESULT_BACKEND = 'redis://192.168.99.100:32770'

CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}

CELERY_REDIS_DB = 0
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']



#from celery import Celery
import celery
#from django.conf import settings

# set the default Django settings module for the 'celery' program.
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'picha.settings')
#app = Celery('stream_framework')
#app = celery.Celery('stream_framework.tasks', broker='redis://localhost/',
#                    backend='redis://localhost:6379/')
#app = celery.Celery('stream_framework.tasks', broker='redis://192.168.99.100:32770/',
#                    backend='redis://192.168.99.100:32770/')
app = celery.Celery('stream_framework.tasks', broker='redis://redis',
                    backend='redis://redis')
current_app = app  # for test suite


# Using a string here means the worker will not have to
# pickle the object when using Windows.
#app.config_from_object('django.conf:settings')
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
        print('Request: {0!r}'.format(self.request))
