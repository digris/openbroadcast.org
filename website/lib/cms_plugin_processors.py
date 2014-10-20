from django.template import Context, Template

def wrap_text(instance, placeholder, rendered_content, original_context):
    '''
    This plugin processor wraps each plugin's output in a colored box if it is in the "main" placeholder.
    '''
    # Plugins not in the main placeholder should remain unchanged
    # Plugins embedded in Text should remain unchanged in order not to break output
    if (instance._render_meta.text_enabled and instance.parent):
        return rendered_content
    else:
        
        
        # For simplicity's sake, construct the template from a string:
        t = Template('<div class="cms_plugin ' + str(instance.plugin_type).lower() + '_holder">{{ content|safe }}</div>')
        # Prepare that template's context:
        c = Context({
            'content': rendered_content,
            # Some plugin models might allow you to customize the colors,
            # for others, use default colors:
            'background_color': instance.background_color if hasattr(instance, 'background_color') else 'lightyellow',
            'border_color': instance.border_color if hasattr(instance, 'border_color') else 'lightblue',
        })
        # Finally, render the content through that template, and return the output
        return t.render(c)