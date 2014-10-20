try:
    from hashlib import md5
except ImportError:
    from md5 import md5

class AratingMiddleware(object):
    def process_request(self, request):
        request.arating_token = self.generate_token(request)

    def generate_token(self, request):
        raise NotImplementedError


class AratingIpMiddleware(AratingMiddleware):
    def generate_token(self, request):
        return request.META['REMOTE_ADDR']

class AratingIpUseragentMiddleware(AratingMiddleware):
    def generate_token(self, request):
        s = ''.join((request.META['REMOTE_ADDR'], request.META['HTTP_USER_AGENT']))
        return md5(s).hexdigest()
