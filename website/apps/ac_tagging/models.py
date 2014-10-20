from tagging.fields import TagField
from django.contrib.admin.widgets import AdminTextInputWidget

from ac_tagging.widgets import TagAutocompleteTagIt


# The following code is based on models.py file from django-tinymce by Joost Cassee

class TagAutocompleteTagItField(TagField):
    """
    TagField with jQuery UI Tag-it widget
    """
    
    def __init__(self, max_tags=False, *args, **kwargs):
        self.max_tags = max_tags
        super(TagAutocompleteTagItField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {'widget': TagAutocompleteTagIt(max_tags=self.max_tags)}
        defaults.update(kwargs)

        # As an ugly hack, we override the admin widget
        if defaults['widget'] == AdminTextInputWidget:
            defaults['widget'] = TagAutocompleteTagIt(max_tags=self.max_tags)

        return super(TagAutocompleteTagItField, self).formfield(**defaults)