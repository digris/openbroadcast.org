from django import template
register = template.Library()

@register.filter
def truncate_chars(value, max_length):

    try:
        if len(value) <= max_length:
            return value

        truncd_val = value[:max_length]
        if value[max_length] != " ":
            rightmost_space = truncd_val.rfind(" ")
            if rightmost_space != -1:
                truncd_val = truncd_val[:rightmost_space]

        return truncd_val + "..."

    except:
        return ''

@register.filter
def truncate_chars_inner(value, max_length):

    try:
        if len(value) - 3 <= max_length: # suptract the "..."
            return value

        offset = 0
        if(value[0:7] == 'http://'):
            offset = 7
        if(value[0:8] == 'https://'):
            offset = 8

        truncd_str = '%s...%s' % (value[offset:int(max_length/2) + offset], value[-int(max_length/2):])

        return truncd_str

    except:
        return ''