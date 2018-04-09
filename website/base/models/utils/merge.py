import logging

from django.db import transaction
from django.db import IntegrityError
from django.apps import apps
from django.db.models import Model
from django.contrib.contenttypes.fields import GenericForeignKey
from tagging.models import Tag

log = logging.getLogger(__name__)

# TODO: investigate if non-atomic transactions here are a problem
#@transaction.atomic
def merge_objects(primary_object, alias_objects=None, keep_old=False):

    """
    Use this function to merge model objects (i.e. Users, Organizations, Polls,
    etc.) and migrate all of the related fields from the alias objects to the
    primary object.

    Usage:
    from django.contrib.auth.models import User
    primary_user = User.objects.get(email='good_email@example.com')
    duplicate_user = User.objects.get(email='good_email+duplicate@example.com')
    merge_objects(primary_user, duplicate_user)
    """

    alias_objects = alias_objects or []

    if not isinstance(alias_objects, list):
        alias_objects = [alias_objects]

    # check that all aliases are the same class as primary one and that
    # they are subclass of model
    primary_class = primary_object.__class__

    if not issubclass(primary_class, Model):
        raise TypeError('Only django.db.models.Model subclasses can be merged')

    for alias_object in alias_objects:
        if not isinstance(alias_object, primary_class):
            pass
            #raise TypeError('Only models of same class can be merged')

    # Get a list of all GenericForeignKeys in all models
    # TODO: this is a bit of a hack, since the generics framework should provide a similar
    # method to the ForeignKey field for accessing the generic related fields.
    generic_fields = []
    for model in apps.get_models():
        for field_name, field in filter(lambda x: isinstance(x[1], GenericForeignKey), model.__dict__.iteritems()):
            generic_fields.append(field)

    blank_local_fields = set([field.attname for field in primary_object._meta.local_fields if getattr(primary_object, field.attname) in [None, '']])

    # Loop through all alias objects and migrate their data to the primary object.
    for alias_object in alias_objects:
        # Migrate all foreign key references from alias object to primary object.
        for related_object in alias_object._meta.get_all_related_objects():
            # The variable name on the alias_object model.
            alias_varname = related_object.get_accessor_name()
            # The variable name on the related model.
            obj_varname = related_object.field.name
            related_objects = getattr(alias_object, alias_varname)
            try:
                for obj in related_objects.all():
                    setattr(obj, obj_varname, primary_object)
                    obj.save()
            except AttributeError as e:
                log.warning('unable to handle "related_objects": {}'.format(e))
                pass

        # Migrate all many to many references from alias object to primary object.
        for related_many_object in alias_object._meta.get_all_related_many_to_many_objects():
            alias_varname = related_many_object.get_accessor_name()
            obj_varname = related_many_object.field.name

            if alias_varname is not None:
                # standard case
                related_many_objects = getattr(alias_object, alias_varname).all()
            else:
                # special case, symmetrical relation, no reverse accessor
                related_many_objects = getattr(alias_object, obj_varname).all()
            for obj in related_many_objects.all():
                getattr(obj, obj_varname).remove(alias_object)
                getattr(obj, obj_varname).add(primary_object)

        # Migrate all generic foreign key references from alias object to primary object.
        for field in generic_fields:
            filter_kwargs = {}
            filter_kwargs[field.fk_field] = alias_object._get_pk_val()
            filter_kwargs[field.ct_field] = field.get_content_type(alias_object)
            for generic_related_object in field.model.objects.filter(**filter_kwargs):
                setattr(generic_related_object, field.name, primary_object)
                try:
                    generic_related_object.save()
                except Exception as e:
                    pass

        # Try to fill all missing values in primary object by values of duplicates
        filled_up = set()
        for field_name in blank_local_fields:
            val = getattr(alias_object, field_name)
            if val not in [None, '']:
                setattr(primary_object, field_name, val)
                filled_up.add(field_name)
        blank_local_fields -= filled_up

        if not keep_old:
            alias_object.delete()
    primary_object.save()
    return primary_object


def merge_votes(primary_object, alias_objects):
    """
    merges votes from 'alias_objects' to the master, taking into account
    that a user can only vote once per object
    """

    for obj in alias_objects:
        for v in obj.votes.all():
            try:
                v.object_id = primary_object.pk
                v.save()
            except IntegrityError as e:
                v.delete()

    return primary_object


def merge_relations(primary_object, alias_objects):
    """
    merges services from 'alias_objects' to the master, taking into account
    that 'specific' services (like wikipedia, musicbrains, etc) can only exist once
    per instance.
    """

    # get available 'specific' relations for the master object
    master_services = [r.service for r in primary_object.relations.exclude(service='generic')]

    for obj in alias_objects:
        # only take specific services into account that are not defined on master
        for r in obj.relations.exclude(service__in=master_services):

            # move to the master object
            r.object_id = primary_object.pk
            r.save()

        # delete 'left over' specific relations
        obj.relations.exclude(service='generic').delete()

    return primary_object


def merge_tags(primary_object, alias_objects):
    """
    merges tags from 'alias_objects' to the master.
    """
    print('merging tags')
    for obj in alias_objects:
        print('slave {}'.format(obj))
        for tag in obj.tags.all():
            print('tag {}'.format(tag))
            Tag.objects.add_tag(primary_object, '"{}"'.format(tag.name))

    print('tags after save', primary_object.tags.all())

    if primary_object.tags.exists():
        primary_object.d_tags = ', '.join(t.name for t in primary_object.tags.all())

    print(primary_object.d_tags)

    return primary_object
