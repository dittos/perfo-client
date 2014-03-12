from time import time
from django.conf import settings
from perfo_client.client import Client

class PerfoMiddleware(object):
    def __init__(self):
        self.client = Client(settings.PERFO_DSN)

    def process_view(self, request, view_func, view_args, view_kwargs):
        request._perfo_start = time()
        request._perfo_key = request.resolver_match.view_name

    def process_response(self, request, response):
        end = time()
        self.client.send('events', {
            'key': request._perfo_key,
            't': [int(request._perfo_start * 1000), int(end * 1000)]
        })
        return response
