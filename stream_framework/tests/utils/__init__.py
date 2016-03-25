from stream_framework.activity import Activity, AggregatedActivity
import six

class FakeActivity(Activity):
    pass

class VixletFakeActivity(Activity):

    def __init__(self, actor, verb, object, target=None, time=None, extra_context=None):
        self.verb = verb
        self.time = time or datetime.datetime.utcnow()
        # either set .actor or .actor_id depending on the data
        self._set_object_or_id('actor', actor)
        self._set_object_or_id('object', object)
        self._set_object_or_id('target', target)
        # store the extra context which gets serialized
        self.extra_context = extra_context or {}
        self.dehydrated = False

    def _set_object_or_id(self, field, object_):
        '''
        Either write the integer to
        field_id
        Or if its a real object
        field_id = int
        field = object
        '''
        id_field = '%s_id' % field
        if isinstance(object_, six.integer_types):
            setattr(self, id_field, object_)
        elif object_ is None:
            setattr(self, field, None)
            setattr(self, id_field, None)
        else:
            setattr(self, field, object_)
            setattr(self, id_field, object_)


class FakeAggregatedActivity(AggregatedActivity):
    pass


class Pin(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
