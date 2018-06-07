
def webpack_devserver(request):

    if hasattr(request, 'webpack_devserver'):
        cxt = {
            'webpack_devserver': request.webpack_devserver
        }
        return cxt

    return {}
