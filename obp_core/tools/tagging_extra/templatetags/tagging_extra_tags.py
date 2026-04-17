import json
from django import template

register = template.Library()


@register.filter
def tag_names_as_json(tags):
    return json.dumps([t.name for t in tags])


@register.filter
def tags_as_json(tags):
    tags = [
        {
            "name": t.name,
            "type": t.type,
        }
        for t in tags.order_by('type', 'name')
    ]
    return json.dumps(tags, indent=2)
