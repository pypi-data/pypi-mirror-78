import json
import falcon
import logging

from tellstick.tdtool import TdTool
from utils import log_msg

class Light(object):
    _tdtool = None

    def __init__(self):
        super().__init__()
        self._tdtool = TdTool()

    def on_get(self, req, resp):
        result = self._tdtool.list_devs()
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp):
        data = json.loads(req.bounded_stream.read())
        log_msg("API put: {}".format(data), level=logging.info, offset=True, color='green')

        result = 'Unknown command'
        status = 'success'
        if data['cmd'] == 'ON':
            result = self._tdtool.on(data['dev'])
        elif data['cmd'] == 'OFF':
            result = self._tdtool.off(data['dev'])
        elif data['cmd'] == 'DIM':
            result = self._tdtool.dim(data['dev'], data['dim'])
        else:
            status = 'error'

        output = {
            'msg' : result
        }
        resp.body = json.dumps(output)
        resp.status = falcon.HTTP_200