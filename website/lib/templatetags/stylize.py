# Jonathan Slenders, City Live

# Based on:
# http://www.djangosnippets.org/snippets/350/

"""
Usage: {% stylize lexer="python" linenostart="10" hl_lines="4" %}...language text...{% endstylize %}

Depends on: Pygments http://pygments.org/

"""

from django.template import Library, Node, resolve_variable
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

register = Library()

class StylizeNode(Node):
    def __init__(self, nodelist, lexer, linenos, linenosstart, hl_lines, noclasses):
        self.nodelist = nodelist
        self.lexer = lexer
        self.linenos = linenos
        self.linenosstart = linenosstart
        self.hl_lines = hl_lines
        self.noclasses = noclasses

    def render(self, context):
        lexer = resolve_variable(self.lexer, context)
        linenosstart = int(resolve_variable(self.linenosstart, context))

        linenos = resolve_variable(self.linenos, context)

        hl_lines = []
        for l in self.hl_lines.split(','):
            try:
                hl_lines.append(int(resolve_variable(l, context)))
            except:
                pass

        return highlight(self.nodelist.render(context),
                    get_lexer_by_name(lexer, encoding='UTF-8'),
                    HtmlFormatter(
                                linenos=linenos,
                                linenostart=linenosstart,
                                hl_lines=hl_lines,
                                noclasses=self.noclasses
                                ))

def stylize(parser, token):
    # Nodelist
    nodelist = parser.parse(('endstylize',))
    parser.delete_first_token()

    # Default options
    linenosstart = "'1'"
    linenos = "'table'" # "'inline'" or "'table'"
    lexer = "'text'"
    hl_lines = ''
    noclasses = False

    # Parse parameters
    bits = token.contents.split()[1:]
    for b in bits:
        if b[0:len('linenos=')] == 'linenos=':
            linenos = b[len('linenos='):]

        if b[0:len('linenostart=')] == 'linenostart=':
            linenosstart = b[len('linenostart='):]

        if b[0:len('lexer=')] == 'lexer=':
            lexer = b[len('lexer='):]

        if b[0:len('hl_lines=')] == 'hl_lines=':
            hl_lines = b[len('hl_lines='):]

        if b == "noclasses":
            noclasses = True

    return StylizeNode(nodelist, lexer, linenos, linenosstart, hl_lines, noclasses)

stylize = register.tag(stylize)