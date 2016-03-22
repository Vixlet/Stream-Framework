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

```docker-compose up```


## build

```
docker build --tag streamframework .
```

## web

```
docker run -d -p 5000:5000 --name sf-flask --link redis streamframework su -m myuser -c "./stream-framework-flask.py"
```

## worker (celery)

```
docker run -d  --name sf-celery --link redis streamframework su -m myuser -c "celery -A stream_framework.tasks worker -l debug --config celery"
```

## run redis

```
docker run -d --name redis -v /Users/abe.kazemzadeh/proj/redis/docker/  -p 32770:6379 redis
```

- sometimes this complains about not having a writable db file

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


# getstream.io endpoints from Anup

The following endpoints are being used:
.connect
.feed
.get
.followMany
.addActivity
.following
.unfollow
.follow
.removeActivity

# running tests

right now I had to manually edit the redis settings to test and
comment out cassandra related tests

```
py.test -sl --tb=short
stream_framework/tests
```