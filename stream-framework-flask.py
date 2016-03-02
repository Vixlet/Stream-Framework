#!/usr/bin/env python
# implement your feed with redis as storage
from collections import namedtuple
import datetime
#import celeryconfig
#from celeryconfig import *
#import celery
from stream_framework.feeds.redis import RedisFeed
from stream_framework.feeds.base import UserBaseFeed
from stream_framework.feed_managers.base import Manager, FanoutPriority, NewManager
from stream_framework.verbs.base import Follow, Comment, Love, Add
from stream_framework.activity import Activity
from stream_framework.feed_managers.base import add_operation
from stream_framework.feeds.aggregated_feed.redis import RedisAggregatedFeed
#app = celery.Celery('stream_framework.tasks', broker='redis://localhost/',
#                    backend='redis://localhost:6379/')


from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

        

manager = NewManager()
manager.follow_user(1,2)

# some activity in Redis (e.g. keys *)
# - create celery list (e.g. LRANGE celery 0 100)
# - create _kombu.bindings.celery set (e.g. SSCAN _kombu.binding.celery 0)
#from stream_framework.verbs import register
#from stream_framework.verbs.base import Verb

from stream_framework.verbs import get_verb_by_id    
for x in range(1,5):
    verb = get_verb_by_id(x)
    print verb

# 1: Follow
# 2: Comment
# 3: Love
# 4: Add
feed1 = RedisFeed(1) 

User = namedtuple('User', ['id'])
a1 = Activity(
    #actor=User("54blablabla"), # some type of mongo user id
    actor=1, # some type of mongo user id
    verb=Follow, # The id associated with the  verb
    object=2, # The id of something/someone
    #target=1, # The id of the Surf Girls board
    time=datetime.datetime.utcnow(), # The time the activity occured
    extra_context={"isn't": "this", "nice": "?", "activity":1}
)

a2 = Activity(
    #actor=User("54blablabla"), # some type of mongo user id
    actor=2, # some type of mongo user id
    verb=Love, # The id associated with the  verb
    object=1, # The id of something/someone
    #target=1, # The id of the Surf Girls board
    time=datetime.datetime.utcnow(), # The time the activity occured
    extra_context={"social": "network", "of": "tomorrow", "activity":2}
)

manager.follow_user(1,2)
#manager.follow_user(1,User)

try:
    manager.add_user_activity(1,a1)
except NotImplementedError:
    print "this is because BaseActivityStorage.add_to_storage is not implemented"


# however, via feed it works
storage = feed1.get_activity_storage()
storage.add_to_storage(storage.serialize_activities([a1]))
    
try:
    manager.add_user_activity(1,a1)
except NotImplementedError:
    print "now the part that isn't implemented is manager.get_user_follower_ids"


operation_kwargs = dict(activities=[a2], trim=True)
priority_group = 'HIGH'
follower_ids = [1,2]
feed_class = manager.feed_classes.values()[0]
#error
#manager.create_fanout_tasks(follower_ids, feed_class, add_operation, operation_kwargs=operation_kwargs, fanout_priority=priority_group)
fanout_task = manager.get_fanout_task(priority_group, feed_class=feed_class)
from stream_framework.utils import chunks
#for x in chunks(follower_ids, 100):
#... 	print x
#follower_ids
user_ids_chunks = follower_ids
chunk_size = 100
#error
#task = fanout_task.delay(feed_manager=manager, feed_class=feed_class, user_ids=follower_ids, operation=add_operation, operation_kwargs=operation_kwargs)


#works?
#task = fanout_task(feed_manager=manager, feed_class=feed_class, user_ids=follower_ids, operation=add_operation, operation_kwargs=operation_kwargs)
#task = fanout_task.delay(feed_manager=manager, feed_class=feed_class, user_ids=follower_ids, operation=add_operation, operation_kwargs=operation_kwargs)
manager.add_user_activity(2,a2)

feed1 = manager.user_feed_class(1)
print feed1[:]

import json

def activity2dict(activity):
    serialization_id = getattr(activity, 'serialization_id')
    actor_id = getattr(activity, 'actor_id')
    verb_id = getattr(activity, 'verb').id
    object_id = getattr(activity, 'object_id')
    time = getattr(activity, 'time')
    return {'serialization_id': serialization_id,
            'actor_id':  actor_id,
            'verb_id': verb_id,
            'object_id':object_id,
            'time': time.isoformat() + 'Z'}

    
class VixletUserFeed(Resource):
    def get(self, user_id):
        feed = manager.user_feed_class(user_id)
        #output = json.dumps(feed[:])
        output = map(activity2dict, feed[:])
        #import pdb; pdb.set_trace()
        return output
    
    
api.add_resource(VixletUserFeed, '/user/<int:user_id>/feed')


if __name__ == '__main__':
    app.run(debug=True)
