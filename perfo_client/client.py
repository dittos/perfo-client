import base64
import json
import urllib2
import urlparse
from perfo_client import version

class Client(object):
    def __init__(self, dsn):
        dsn = urlparse.urlparse(dsn)
        self.base_url = '%s://%s:%d%s' % (dsn.scheme, dsn.hostname, dsn.port, dsn.path)
        key = base64.encodestring('%s:%s' % (dsn.username, dsn.password))
        key = key.replace('\n', '')
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Perfo-client/%s' % version,
            'Authorization': 'Basic %s' % key,
        }

    def send(self, path, data):
        req = urllib2.Request(
            url=self.base_url + '/' + path,
            data=json.dumps(data),
            headers=self.headers,
        )
        resp = urllib2.urlopen(req)
        result = resp.read()
        resp.close()
