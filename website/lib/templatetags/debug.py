# Author: Jonathan Slenders

from cgi import escape
import sys

from django import template
from django.conf import settings
from django.template import Node, Template, resolve_variable
from django.template import Context

# Tools for debugging django templates

# - {% repr %} : prints information about this variable
# - {% raise "exception" %} : raises an exception with this message
# - {% try %} ... ( {% except %} ... ) {% endtry %} :
#          Similar to the try/except structure of Python, but
#          Shows a nice traceback when the {% except %} block is missing
#
# e.g.
# {% load debug %}
# {% try %}
#     {% something which could cause an error ... %}
#     - or -
#     {% raise "error message" %}
# {% except %}
#     {% exception ... %}
# {% endtry %}


register = template.Library()

# ==============[  repr  ]===================

def _escape(a):
    try:
        return escape(str(a))
    except:
        return '(error...)'

def _e(*args):
    return tuple([ _escape(a) for a in args ])


class PrintNode(Node):
    def __init__(self, var):
        self.var = var

    def render(self, context):
        try:
            var = resolve_variable(self.var, context)

            if isinstance(var, dict):
                d = var
            else:
                d = var.__dict__
            try: module = var.__module__
            except: module = ''

            dict2 = []
            for v in d:
                dict2.append(u'<tr><td>%s</td><td>%s</td></tr>' % _e(v, d[v]))
            dict2 = u'<table style="background-color: white;">%s</table>' % ''.join(dict2)
            dict2 = dict2.replace('%', '%%')

            return (
            u'<table style="background-color: #eeeeee; width: 80%%; margin: auto; border: 1px solid black;">'
                u'<tr><th>Variable:</th><td>%s</td></tr>'
                u'<tr><th>Class name:</th><td>%s</td></tr>'
                u'<tr><th>Module path:</th><td>%s</td></tr>'
                u'<tr><th>__dict__:</th><td>' + dict2 + u'</td></tr>'
                u'<tr><th>dir(__class__):</th><td>%s</td></tr>'
            u'</table>') % _e(self.var, var.__class__.__name__, module, str(dir(var.__class__)))
        except Exception, e:
            return '<strong>%s has not been defined (%s)</strong>' % _e(self.var, e.__class__.__name__)

@register.tag
def repr(parser, token):
    args = token.split_contents()

    if len(args) == 2:
        return PrintNode(args[1])
    else:
        raise template.TemplateSyntaxError


# ==============[  try/catch ]===================

class Frame(object):
    def __init__(self, filename, line, locals, is_template):
        self.filename = filename
        self.line = line
        self.locals = locals
        self.is_template = is_template

        try:
            self._content = open(filename, 'r').read()
        except Exception, e:
            # filename can equal u'<string>'
            self._content = ''

    @property
    def surrounding_content(self):
        line = self.line

        # Don't ever return 'negative' lines
        while line < 4:
            line += 1

        def no_empty_lines(line):
            # Replace empty lines by a space. (stylize trims newlines)
            return line or ' '

        return '\n'.join(map(no_empty_lines, self._content.split('\n')[ line - 2: line + 1]))

    @property
    def surrounding_content_first_line(self):
        return max(0, self.line - 1)


    @property
    def surrounding_content_highlighted_line(self):
        return self.line if self.line < 2 else 2


error_template = \
"""
{% load stylize %}
<div class="template-traceback">
    <p style="font-weight: bold; text-align: center; font-size: 120%;">Error</p>
    <p>
        Caught in: <em style="padding: 0 2em;font-weight:bold;">{{ filename }}</em> ({{ frames|length }}&nbsp;frames)
    </p>
    <div style="background-color: white; overflow:auto; border: 1px solid #dddddd">
    <table>
    {% for f in frames %}
        <tr>
            {% if forloop.last %}<td style="border-left: 4px solid black;">{% else %}<td>{% endif %}
            {% if forloop.last %}<strong>{% else %} <em style="color: #444444;">{% endif %}
            {{ f.filename }}
            {% if forloop.last %}</strong>{% else %}</em>{% endif %} : {{ f.line }}
            {% if f.is_template %}
                {% stylize lexer="django" hl_lines=f.surrounding_content_highlighted_line linenostart=f.surrounding_content_first_line %}{{ f.surrounding_content|safe }}{% endstylize %}
            {% else %}
                {% stylize lexer="python" hl_lines=f.surrounding_content_highlighted_line linenostart=f.surrounding_content_first_line %}{{ f.surrounding_content|safe }}{% endstylize %}
            {% endif %}
            </td>
        </tr>
    {% endfor %}
    </table>
    {% stylize lexer="pytb" %}{{ exception|safe }}{% endstylize %}
    </div>
</div>
"""

class TryNode(Node):
    def __init__(self, tryblock, exceptblock):
        self.tryblock = tryblock
        self.exceptblock = exceptblock

    def render(self, context):
        if getattr(settings, 'DEBUG', False):
            # Do try/catch in case of debug
            try:
                return self.tryblock.render(context)
            except Exception, e:
                if self.exceptblock:
                    return self.exceptblock.render(context)
                else:
                    return Template(error_template).render(Context(
                            {
                                'filename': self.source[0].name,
                                'frames': self.display_exception(e),
                                'exception': str(e)
                            }))
        else:
            return self.tryblock.render(context)

    def get_nodes_by_type(self, nodetype):
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        nodes.extend(self.tryblock.get_nodes_by_type(nodetype))
        if self.exceptblock:
            nodes.extend(self.exceptblock.get_nodes_by_type(nodetype))
        return nodes


    def display_exception(self, exception):
        tb = sys.exc_info()[2]
        frames = []

        # Skip first frame, but show {% try %} block instead
        tb = tb.tb_next

        filename, origin = self.source
        filename = filename.name
        lineno = self.get_line_number_for_template(filename, origin[0])
        frames.append(Frame(filename, lineno, [], True))

        # Iterate over frames
        while tb:
            frame = tb.tb_frame

            # support for __traceback_hide__ which is used by a few libraries
            # to hide internal frames.
            # See also: site-packages/django/views/debug.py
            if tb.tb_frame.f_locals.get('__traceback_hide__'):
                tb = tb.tb_next
                continue

            # Read information from frame
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            is_template = False

            # If this is a template-frame, replace file and line number by
            # their corresponding template information
            if 'django/template/__init__.py' in filename:
                try:
                    filename, origin = frame.f_locals['node'].source
                    filename = filename.name
                    lineno = self.get_line_number_for_template(filename, origin[0])
                    is_template = True
                except Exception, e:
                    pass

            # Don't show (other) frames from in the django framework
            if 'django/template' in filename:
                pass

            # Show own frames and templates
            else:
                locals = []

                for name, value in frame.f_locals.items():
                    locals.append({ 'name': name, 'value': value })

                frames.append(Frame(filename, lineno, locals, is_template))

            tb = tb.tb_next

        return frames

    def get_line_number_for_template(self, filename, index):
        # lineo points to a byte instead of a line
        # calculate line number
        count = index
        n = 1

        for line in open(filename, 'r').read().split('\n'):
            count -= len(line) + 1

            if count <= 0:
                return n

            n += 1

        return n


@register.tag(name='try')
def try_(parser, token):
    """
    {% try %} content nodes {% except %} content nodes {% endtry %}
    """
    # Read try block
    tryblock = parser.parse(('except', 'endtry'))
    exceptblock = None

    if parser.tokens[0].contents == 'except':
        parser.delete_first_token()

        exceptblock = parser.parse(('endtry',))
        parser.delete_first_token()
    else:
        parser.delete_first_token()
    print 'parsed try block'

    # Return meta node
    return TryNode(tryblock, exceptblock)


# ==============[  raise ]===================


class RaiseNode(Node):
    def __init__(self, message):
        self.message = message

    def render(self, context):
        raise Exception(str(self.message))


@register.tag(name='raise')
def raise_(parser, token):
    """
    {% raise "message" %}
    """
    args = token.split_contents()

    if len(args) == 2:
        return RaiseNode(args[1])
    else:
        raise template.TemplateSyntaxError
