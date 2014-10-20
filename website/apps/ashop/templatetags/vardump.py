import cgi

from django import template


register = template.Library()

@register.tag
def vardump(parser, token):
    tagname, varname = token.contents.split()
    return VardumpRenderer(varname)

class VardumpRenderer(template.Node):
    def __init__(self, var):
        self.var = var
    def render(self, context):
        var = self.var
        try:
            var = template.resolve_variable(self.var, context)
            t = type(var)
            return cgi.escape("%s => %s" % (t, var))
            
            #return vars(var)
        
        except template.VariableDoesNotExist:
            return 'VariableDoesNotExist'
