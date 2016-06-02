"""
Not used anymore. but file should stay for the moment as UUIDField appears in migrations
"""
import uuid

from django.db.models import CharField

UUID_BASE_ID = 'fff0'
UUID_BASE_VERSION = 4
UUID_BASE_NAME = 'anorg.net'
UUID_BASE_NAMESPACE = uuid.NAMESPACE_DNS
    
class UUIDVersionError(Exception):
    pass


class UUIDField(CharField):
    """ UUIDField

    By default uses UUID version 1 (generate from host ID, sequence number and current time)

    The field support all uuid versions which are natively supported by the uuid python module.
    For more information see: http://docs.python.org/lib/module-uuid.html
    """

    def __init__(self, verbose_name=None, name=None, auto=True, version=UUID_BASE_VERSION, node=None, clock_seq=None, namespace=None, **kwargs):
        kwargs['max_length'] = 36
        if auto:
            kwargs['blank'] = True
            kwargs.setdefault('editable', False)
        self.auto = auto
        self.version = version
        if version == 1:
            self.node, self.clock_seq = node, clock_seq
        elif version == 3 or version == 5:
            self.namespace, self.name = namespace, name
        CharField.__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        return CharField.__name__

    def contribute_to_class(self, cls, name):
        if self.primary_key:
            assert not cls._meta.has_auto_field, \
              "A model can't have more than one AutoField: %s %s %s; have %s" % \
               (self, cls, name, cls._meta.auto_field)
            super(UUIDField, self).contribute_to_class(cls, name)
            cls._meta.has_auto_field = True
            cls._meta.auto_field = self
        else:
            super(UUIDField, self).contribute_to_class(cls, name)

    def create_uuid(self):

        if not self.version or self.version == 4:
            res = uuid.uuid4()
        elif self.version == 1:
            res = uuid.uuid1(self.node, self.clock_seq)
        elif self.version == 2:
            raise UUIDVersionError("UUID version 2 is not supported.")
        elif self.version == 3:
            res = uuid.uuid3(self.namespace, self.name)
        elif self.version == 5:
            res = uuid.uuid5(UUID_BASE_NAMESPACE, UUID_BASE_NAME)
        else:
            raise UUIDVersionError("UUID version %s is not valid." % self.version)


        #if UUID_BASE_ID:
        #    res = "%s%s" % (UUID_BASE_ID, str(res)[4:])
        
        return res
        

    def pre_save(self, model_instance, add):
        value = super(UUIDField, self).pre_save(model_instance, add)
        if self.auto and add and value is None:
            value = unicode(self.create_uuid())
            setattr(model_instance, self.attname, value)
            return value
        else:
            if self.auto and not value:
                value = unicode(self.create_uuid())
                setattr(model_instance, self.attname, value)
        return value

