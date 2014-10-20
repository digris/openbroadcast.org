from django import template
from django.contrib.contenttypes.models import ContentType

from genericrelations.models import RelatedContent

register = template.Library()


"""
a = Article.objects.get(pk=1)
ct = ContentType.objects.get_for_model(a)

UP:
rc = RelatedContent.objects.filter(content_type__pk=ct.id,object_id=a.id)

DOWN:
rc = RelatedContent.objects.filter(parent_content_type=ct,parent_object_id=a.id)

rc[0].content_object.get_absolute_url()
"""
@register.filter
def classname(obj, arg=None):
    classname = obj.__class__.__name__.lower()
    if arg:
        if arg.lower() == classname:
            return True
        else:
            return False
    else:
        return classname


@register.tag("get_related")
def get_related(parser, token):
    
    try:
        tag_name, item = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly one argument: the ct-object" % token.contents.split()[0])
    
    return ObjectRelationNode(item)
    return "..."


class ObjectRelationNode(template.Node):
    def __init__(self, item):

        self.item = template.Variable(item)
        
    def render(self, context):
        
        item = self.item.resolve(context)
        ct = ContentType.objects.get_for_model(item)
        
        rcus = RelatedContent.objects.filter(content_type=ct,object_id=item.id)
        rcds = RelatedContent.objects.filter(parent_content_type=ct,parent_object_id=item.id)
            
        ru = []
        rd = []
        
        rr = []
        ra = []
        for rc in rcus:
            ru.append(rc.parent_content_object) #
        for rc in rcds:
            if rc.content_type.name not in ['Release', 'Artist']:
                rd.append(rc.content_object)
            if rc.content_type.name == 'Release':
                rr.append(rc.content_object)
            if rc.content_type.name == 'Artist':
                ra.append(rc.content_object)
            
        

        context['related_up'] = ru
        context['related_down'] = rd
        
        context['related_releases'] = rr
        context['related_artists'] = ra

        return ''

