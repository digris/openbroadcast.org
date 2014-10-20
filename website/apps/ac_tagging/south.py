from south.modelsinspector import add_introspection_rules
from django.conf import settings

if "ac_tagging" in settings.INSTALLED_APPS:
    try:
        from ac_tagging.models import TagAutocompleteTagItField
    except ImportError:
        pass
    else:
        rules = [
            (
                (TagAutocompleteTagItField, ),
                [],
                {
                    "blank": ["blank", {"default": True}],
                    "max_length": ["max_length", {"default": 255}],
                    "max_tags": ["max_tags", {"default": False}],
                },
            ),
        ]
        add_introspection_rules(rules, ["^ac_tagging\.models",])