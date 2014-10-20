from django.db.models.deletion import Collector
from django.db.models.fields.related import ForeignKey

def duplicate(obj, value=None, field=None, duplicate_order=None):
    """
    Duplicate all related objects of obj setting
    field to value. If one of the duplicate
    objects has an FK to another duplicate object
    update that as well. Return the duplicate copy
    of obj.
    duplicate_order is a list of models which specify how
    the duplicate objects are saved. For complex objects
    this can matter. Check to save if objects are being
    saved correctly and if not just pass in related objects
    in the order that they should be saved.
    """
    collector = Collector({})
    collector.collect([obj])
    collector.sort()
    related_models = collector.data.keys()
    data_snapshot =  {}
    for key in collector.data.keys():
        data_snapshot.update({ key: dict(zip([item.pk for item in collector.data[key]], [item for item in collector.data[key]])) })
    root_obj = None

    # Sometimes it's good enough just to save in reverse deletion order.
    if duplicate_order is None:
        duplicate_order = reversed(related_models)

    for model in duplicate_order:
        # Find all FKs on model that point to a related_model.
        fks = []
        for f in model._meta.fields:
            if isinstance(f, ForeignKey) and f.rel.to in related_models:
                fks.append(f)
        # Replace each `sub_obj` with a duplicate.
        if model not in collector.data:
            continue
        sub_objects = collector.data[model]
        for obj in sub_objects:
            for fk in fks:
                fk_value = getattr(obj, "%s_id" % fk.name)
                # If this FK has been duplicated then point to the duplicate.
                fk_rel_to = data_snapshot[fk.rel.to]
                if fk_value in fk_rel_to:
                    dupe_obj = fk_rel_to[fk_value]
                    setattr(obj, fk.name, dupe_obj)
            # Duplicate the object and save it.
            obj.id = None
            if field is not None:
                setattr(obj, field, value)
            try:
                obj.save()
            except:
                pass
            if root_obj is None:
                root_obj = obj
    return root_obj