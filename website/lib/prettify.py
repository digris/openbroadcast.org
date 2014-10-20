import tidylib
from tidylib import tidy_document




tidylib.BASE_OPTIONS = {
    "output-xhtml": 1,     # XHTML instead of HTML4
    "indent": 1,           # Pretty; not too much of a performance hit
    "tidy-mark": 0,        # No tidy meta tag in output
    "tab-size": 1,        # No tidy meta tag in output
    "wrap": 500,             # No wrapping
    "alt-text": "",        # Help ensure validation
    "doctype": 'strict',   # Little sense in transitional for tool-generated markup...
    "force-output": 1,     # May not get what you expect but you will get something
    "hide-comments": 1,     # May not get what you expect but you will get something
    }


class PrettifyMiddleware(object):
    """Prettify middleware"""

    def process_response(self, request, response):
        
        
        print response['Content-Type']
        
        """"""
        if response['Content-Type'].split(';', 1)[0] == 'text/html':
            content = response.content
            # content = str(tidy.parseString(content, **options))
            # content, errors = tidy_document(content, options={'numeric-entities':1})
            # print errors
            response.content = content
            
            
        return response
