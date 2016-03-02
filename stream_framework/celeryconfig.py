## Broker settings.
#BROKER_URL = 'redis://localhost:6379'
BROKER_URL = 'redis://192.168.99.100:32770'

# List of modules to import when celery starts.
#CELERY_IMPORTS = ('myapp.tasks', )

## Using the database to store task state and results.
#CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://192.168.99.100:32770'

CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}

CELERY_REDIS_DB = 0
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
