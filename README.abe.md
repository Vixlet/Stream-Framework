# running things locally

## run redis

in redis directory
```
src/redis-server
```

## run celery

```
celery -A stream_framework.tasks worker -l debug --config celery
```

## run server

```
./stream-framework-flask.py
```


# using docker

eventually ```docker-compose``` but also individual commands below


## build
docker build --tag streamframework .

## web
docker run -it --rm --streamframework stream-framework-flask.py

## worker
docker run -it --rm --streamframework 

## run redis
```
docker run -d -v /Users/abe.kazemzadeh/proj/redis/docker/ --name redis -p 32770:6379 redis
```

## run celery

# config

configures server (celery client)
```
stream_framework/default_settings.py
```

configures celery worker
```
(actually not 100% sure)
stream_framework/celery.py
stream_framework/celeryconfig.py
celeryconfig.py
```




# some redis commands

run command-line interface
```
src/redis-cli
```


list all keys
```
keys *
```

delete all keys
```
EVAL "return redis.call('del', unpack(redis.call('keys', ARGV[1])))" 0 *
```

get elements of hash
```
HGETALL key
```

get values of weighted set
```
zrange key 0 100 [withscores]
```

and of course for a simple key-value object
```
get key
```


