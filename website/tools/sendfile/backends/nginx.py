from django.http import HttpResponse

from _internalredirect import _convert_file_to_url

def sendfile(request, filename, **kwargs):

    print 'nginx - sendfile'

    #print 'filename:           %s' % filename
    #print 'converted filename: %s' % _convert_file_to_url(filename)

    response = HttpResponse()
    response['X-Accel-Redirect'] = _convert_file_to_url(filename)

    return response
