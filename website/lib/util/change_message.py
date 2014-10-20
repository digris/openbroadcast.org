from django.utils.text import get_text_list
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _

def construct(request, form, formsets):
    """
    Construct a change message from a changed object.
    """
    change_message = []
    if form.changed_data:
        
        try:
            form.changed_data.remove('d_tags')
        except:
            pass
            
        if len(form.changed_data) > 0:
            #change_message.append(_('Changed %s. \n') % get_text_list(form.changed_data, _('and')))
            change_message.append(_('Changed %s. \n') % get_text_list(convert_changed_list(form.instance, form.changed_data), _('and')))



    if formsets:
        try:
            for formset in formsets:
                for added_object in formset.new_objects:
                    change_message.append(_('Added %(name)s "%(object)s". \n')
                                          % {'name': force_unicode(added_object._meta.verbose_name),
                                             'object': force_unicode(added_object)})



                # remove some 'wrong' messages

                co = formset.changed_objects
                """
                for el in formset.changed_objects:
                    if el[0].__class__.__name__ == 'Media':
                        if el[0].release.publish_date:
                            if 'license' in el[1]: el[1].remove('license')
                    if len(el[1]) < 1:
                        co.remove(el)
                """


                for changed_object, changed_fields in co:

                    # hakish... somehow we have to exclude certain messages
                    skip = False
                    if changed_object.__class__.__name__ == 'Relation':
                        if 'service' in changed_fields:
                            #pass
                            skip = True

                    if changed_object.__class__.__name__ == 'Media':
                        if 'license' in changed_fields:
                            if changed_object.release.publish_date:
                                pass
                                #skip = True


                    if not skip:
                        change_message.append(_('Changed %(list)s for %(name)s "%(object)s". \n')
                                              % {'list': get_text_list(changed_fields, _('and')),
                                                 'name': force_unicode(changed_object._meta.verbose_name),
                                                 'object': force_unicode(changed_object)})

                for deleted_object in formset.deleted_objects:
                    change_message.append(_('Deleted %(name)s "%(object)s". \n')
                                          % {'name': force_unicode(deleted_object._meta.verbose_name),
                                             'object': force_unicode(deleted_object)})
        except Exception, e:
            print e
            pass

    change_message = ' '.join(change_message)
    return change_message or _('Nothing changed')





def convert_changed_list(obj, changed_data):
    cls = type(obj)
    verbose_names = []
    for field in changed_data:
        try:
            verbose_names.append(cls._meta.get_field_by_name(field)[0].verbose_name)
        except Exception:
            verbose_names.append(field)
    return verbose_names




def parse_tags(obj, d_tags, msg=''):

    try:

        d_tags = ['"%s"' % x.strip() for x in d_tags.split(',')]
        tags = ['"%s"' % x.name for x in obj.tags]

        tags_added = diff_lists(d_tags, tags)
        tags_removed = diff_lists(tags, d_tags)

        if (tags_added or tags_removed) and msg == 'Nothing changed':
            msg = _('Changed: \n')

        if tags_added:
            msg += _('Tags added: %s' % get_text_list(tags_added, _('and')))

        if tags_added and tags_removed:
            msg += '\n'

        if tags_removed:
            msg += _('Tags removed: %s' % get_text_list(tags_removed, _('and')))

        return msg

    except:
        return ''


def diff_lists(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]