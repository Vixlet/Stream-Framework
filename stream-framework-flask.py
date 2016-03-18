#!/usr/bin/env python
# implement your feed with redis as storage
import logging
logging.basicConfig(level=logging.DEBUG)

from collections import namedtuple
import datetime
import re
#import celeryconfig
#from celeryconfig import *
#import celery
from stream_framework.feeds.redis import RedisFeed
from stream_framework.feeds.base import UserBaseFeed
from stream_framework.feed_managers.base import Manager, FanoutPriority, NewManager
from stream_framework.verbs.base import Follow, Comment, Love, Add, Verb
from stream_framework.activity import Activity
from stream_framework.feed_managers.base import add_operation
from stream_framework.feeds.aggregated_feed.redis import RedisAggregatedFeed
#app = celery.Celery('stream_framework.tasks', broker='redis://localhost/',
#                    backend='redis://localhost:6379/')
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

        

manager = NewManager()
#manager.follow_user(1,2)

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
#feed1 = RedisFeed(1) 

# User = namedtuple('User', ['id'])
# a1 = Activity(
#     #actor=User("54blablabla"), # some type of mongo user id
#     actor=1, # some type of mongo user id
#     verb=Follow, # The id associated with the  verb
#     object=2, # The id of something/someone
#     #target=1, # The id of the Surf Girls board
#     time=datetime.datetime.utcnow(), # The time the activity occured
#     extra_context={"isn't": "this", "nice": "?", "activity":1}
# )

# a2 = Activity(
#     #actor=User("54blablabla"), # some type of mongo user id
#     actor=2, # some type of mongo user id
#     verb=Love, # The id associated with the  verb
#     object=1, # The id of something/someone
#     #target=1, # The id of the Surf Girls board
#     time=datetime.datetime.utcnow(), # The time the activity occured
#     extra_context={"social": "network", "of": "tomorrow", "activity":2}
# )

# manager.follow_user(1,2)
#manager.follow_user(1,User)

# try:
#     manager.add_user_activity(1,a1)
# except NotImplementedError:
#     print "this is because BaseActivityStorage.add_to_storage is not implemented"


# # however, via feed it works
# storage = feed1.get_activity_storage()
# storage.add_to_storage(storage.serialize_activities([a1]))
    
# try:
#     manager.add_user_activity(1,a1)
# except NotImplementedError:
#     print "now the part that isn't implemented is manager.get_user_follower_ids"


# operation_kwargs = dict(activities=[a2], trim=True)
# priority_group = 'HIGH'
# follower_ids = [1,2]
# feed_class = manager.feed_classes.values()[0]
# #error
# #manager.create_fanout_tasks(follower_ids, feed_class, add_operation, operation_kwargs=operation_kwargs, fanout_priority=priority_group)
# fanout_task = manager.get_fanout_task(priority_group, feed_class=feed_class)
# from stream_framework.utils import chunks
# #for x in chunks(follower_ids, 100):
# #... 	print x
# #follower_ids
# user_ids_chunks = follower_ids
# chunk_size = 100
# #error
# #task = fanout_task.delay(feed_manager=manager, feed_class=feed_class, user_ids=follower_ids, operation=add_operation, operation_kwargs=operation_kwargs)


# #works?
# #task = fanout_task(feed_manager=manager, feed_class=feed_class, user_ids=follower_ids, operation=add_operation, operation_kwargs=operation_kwargs)
# #task = fanout_task.delay(feed_manager=manager, feed_class=feed_class, user_ids=follower_ids, operation=add_operation, operation_kwargs=operation_kwargs)
# manager.add_user_activity(2,a2)

# feed1 = manager.user_feed_class(1)
# print feed1[:]

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

parser = reqparse.RequestParser()
parser.add_argument('data')


import uuid
def serialize(activity):
    #activity['id'] = str(uuid.uuid1())
    #activity['time'] = str(datetime.datetime.now())
    return json.dumps(activity)
#def deserialize(serialized_activity):
#    return json.loads(serialized_activity, object_hook=json_util.object_hook)
def add_operation2(feed, activities, trim=True):
    '''
    Add the activities to the feed
    functions used in tasks need to be at the main level of the module
    '''
    #t = timer()
    msg_format = 'running %s.add_many operation for %s activities batch interface %s and trim %s'
    print feed, len(activities)
    #feed.add_many(activities, trim=trim)
    #serialized_activities = serialize_activities(activities)
    serialized_activities = {}
    for a in activities:
        serialized = serialize(a)
        #serialized_activities[a['id']] = serialized
        serialized_activities[a['serialization_id']] = serialized
    #add_to_storage(serialized_activities, *args, **kwargs)
    print serialized_activities
    storage = feed.get_activity_storage()
    print storage, dir(storage)
    res = storage.add_to_storage(serialized_activities)
    storage = feed.get_timeline_storage()
    print storage, dir(storage)
    res = storage.add_to_storage(feed.user_id, serialized_activities)
    print "res", res
    print "done add_operation2"
    #print 'add many operation took %s seconds' % t.next()

class VixletFeed(Resource):
    def get(self, feed_id):
        feed = manager.user_feed_class(feed_id)
        #import pdb; pdb.set_trace()
        feed.key = feed_id
        #output = json.dumps(feed[:])
        #output = map(activity2dict, feed[:])
        res = feed.get_activity_slice(0,10,False)
        output = []
        #import pdb; pdb.set_trace()
        for r in res:
            # this is weird
            output.append(json.loads(r.serialization_id))
        print "output", output
        
        return {"duration":0,
                "results": output,
                "next": ""}
    def gget(self, feed_id):
        #m = re.match(r"(?P<prefix>[^_]+)_(?P<domain_id>[^_]+)_(?P<subworld_id>[^_]+)_(?P<user_id>[^_]+)_(?P<qualifier>[^_]*)", feed_id)
        #print m.group('prefix'), m.group('domain_id'), \
            #m.group('subworld_id'), m.group('userid'), \
            #m.group('qualifier')
        print "feed_id", feed_id
        feed = manager.get_feeds(feed_id)['normal']
        print "feed", feed
        #feed = manager.user_feed_class(feed_id)
        #output = map(activity2dict, feed[:])
        res = feed.get_activity_slice(0,10,False)
        print "res", res
        activity_ids = []
        for activity in res:
            activity_ids += activity._activity_ids
        activity_list = feed.activity_storage.get_many(activity_ids)
        from stream_framework.storage.redis.structures.hash import ShardedHashCache
        class ActivityCache(ShardedHashCache): key_format = 'activity:cache:%s'
        cache = ActivityCache(feed.activity_storage.options.get('key', 'normal'))
        output = cache.get_many(activity_ids)
        #import pdb; pdb.set_trace()
        #output = {u'duration': u'18ms', u'results': [{u'origin': u'feed:capsule_55dd08a6355b5bbc1f108ee7_official', u'target': None, u'object': u'24iqNvsZDzJ', u'actor': u'5593481a43bbff4f77bf75a2', u'to': [], u'verb': u'posted', u'capsule_id': u'55dd08a6355b5bbc1f108ee7', u'time': datetime.datetime(2016, 2, 10, 2, 35, 36, 184889).isoformat(), u'foreign_id': u'24iqNvsZDzJ', u'id': u'f715c23a-cf9e-11e5-8080-80014e0979e1'}], u'next': u'/api/v1.0/feed/feed/user_9_0_5600c2359e08b6b9653ce87e_official/?id_lt=f715c23a-cf9e-11e5-8080-80014e0979e1&api_key=5e62adrfbcxw&limit=1&offset=0'}
        res = {"results": output,
               "duration": 0,
               "next": ""}
        return res

    def post(self, feed_id):
        print feed_id
        args = parser.parse_args()
        j = request.get_json()
        #{u'verb': u'posted', u'actor': u'user_6_offu1_my', u'object': u'24iqNvsZDzJ'}
        IdObj = namedtuple('IdObj', ['id'])
        activity = Activity(
            actor=IdObj(j['actor']),
            verb=Add, 
            object=IdObj(j['object']), 
            time=datetime.datetime.utcnow(),
            extra_context={"isn't": "this", "nice": "?", "activity":1}
        )
        print "json, activity, dir(activity)", j, activity, dir(activity)
        feed = manager.feed_classes['normal'](feed_id)
        print feed
        #j['serialization_id'] = activity.serialization_id
        from stream_framework.utils import make_list_unique, datetime_to_epoch
        #j['serialization_id'] = '%s%0.10d%0.3d ' % str(int(datetime_to_epoch(activity.time)) * 1000)
        j['serialization_id'] = str(int(datetime_to_epoch(activity.time)) * 1000)
        print add_operation2(feed, [j])
        print "serialization_id", str(int(datetime_to_epoch(activity.time)) * 1000)
        #print add_operation2(feed, [activity])
        return j

    
    
api.add_resource(VixletUserFeed, '/user/<int:user_id>/feed')
#api.add_resource(VixletUserFeed, '/api/v1.0/feed/feed/user_<int:domain_id>_<int:subworld_id>_<user_id>_<stream_qualifier>')
api.add_resource(VixletFeed,
                 '/api/v1.0/feed/feed/<feed_id>',
                 '/api/v1.0/feed/feed/<feed_id>/',
                 '/api/v1.0/feed/<feed_id>',
                 '/api/v1.0/feed/<feed_id>/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    #app.run(host='0.0.0.0')
