from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class BaseActivity(Model):
    feed_id = columns.Ascii(primary_key=True, partition_key=True)
    activity_id = columns.VarInt(primary_key=True, clustering_order='desc')


class Activity(BaseActivity):
    actor = columns.Integer(required=False)
    extra_context = columns.Bytes(required=False)
    object = columns.Integer(required=False)
    target = columns.Integer(required=False)
    time = columns.DateTime(required=False)
    verb = columns.Integer(required=False)


class AggregatedActivity(BaseActivity):
    activities = columns.Bytes(required=False)
    created_at = columns.DateTime(required=False)
    group = columns.Ascii(required=False)
    updated_at = columns.DateTime(required=False)

class VixletActivity(Model):
    feed_id = columns.Ascii(primary_key=True, partition_key=True)
    activity_id = columns.Ascii(primary_key=True,
                                clustering_order='desc')
    actor = columns.Ascii(required=False)
    object = columns.Ascii(required=False)
    capsule = columns.Ascii(required=False)
    time = columns.DateTime(required=False)
    verb = columns.Ascii(required=False)
    #extra_context = columns.Bytes(required=False)
