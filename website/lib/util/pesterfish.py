##  Copyright (c) 2010 Jacob Smullyan

##  Permission is hereby granted, free of charge, to any person
##  obtaining a copy of this software and associated documentation
##  files (the "Software"), to deal in the Software without
##  restriction, including without limitation the rights to use,
##  copy, modify, merge, publish, distribute, sublicense, and/or sell
##  copies of the Software, and to permit persons to whom the
##  Software is furnished to do so, subject to the following
##  conditions:

##  The above copyright notice and this permission notice shall be
##  included in all copies or substantial portions of the Software.

##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
##  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
##  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
##  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
##  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
##  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
##  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
##  OTHER DEALINGS IN THE SOFTWARE.

"""

A convention for marshalling XML as JSON, based on elementtree, and
written in reaction to badgerfish (http://badgerfish.ning.com/).

An xml element is represented as a dictionary with the keys:

    * tag
    * attributes
    * text
    * tail
    * children

"""


try:
    from xml.etree.cElementTree import Element
except ImportError:
    try:
        from xml.etree.ElementTree import Element
    except ImportError:
        try:
            from cElementTree import Element
        except ImportError:
            try:
                from lxml.etree import Element
            except ImportError:
                from elementtree.ElementTree import Element
            
import simplejson

def elem_to_pesterfish(elem):
    """
    turns an elementtree-compatible object into a pesterfish dictionary
    (not json).
    
    """
    d=dict(tag=elem.tag)
    if elem.text:
        d['text']=elem.text
    if elem.attrib:
        d['attributes']=elem.attrib
    children=elem.getchildren()
    if children:
        d['children']=map(elem_to_pesterfish, children)
    if elem.tail:
        d['tail']=elem.tail
    return d

def pesterfish_to_elem(pfsh, factory=Element):
    """
    turns a pesterfish dictionary (not json!) into an elementtree
    Element.  Whatever Element implementation we could import will be
    used by default; if you want to use something else, pass the
    Element class as the factory parameter.
    """
    
    e=factory(pfsh['tag'], pfsh.get('attributes', {}))
    e.text=pfsh.get('text', "")
    e.tail=pfsh.get('tail', "")
    for c in pfsh.get('children', ()):
        e.append(pesterfish_to_elem(c))
    return e
    
                   
def to_pesterfish(elem):
    """
    turns an elementtree-compatible element or tree
    into a pesterfish json string.
    
    """
    if hasattr(elem, 'getroot'):
        elem=elem.getroot()
    return simplejson.dumps(elem_to_pesterfish(elem))

def from_pesterfish(json, factory=Element):
    """
    turns a pesterfish json string into an elementtree Element.
    Whatever Element implementation we could import will be used by
    default; if you want to use something else, pass the Element class
    as the factory parameter.
    """
    return pesterfish_to_elem(simplejson.loads(json), factory)
    

            
    
    
