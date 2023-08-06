# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from wsgiref import simple_server
import falcon
import os
import json
import sys

from warpseq.server.mailbox import Mailbox, Message
from warpseq.server.packet import CommandPacket
from warpseq.api.public import Api as WarpApi
from warpseq.server.templar import Templar
from warpseq.server.page_builder import PageBuilder
from warpseq.api.exceptions import TimeoutException

#=======================================================================================================================

class BaseResource(object):

    __slots__ = ('mailbox')

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, mailbox=None):
        self.mailbox = mailbox

    # ------------------------------------------------------------------------------------------------------------------

    def _send_to_engine(self, data):
        return self.mailbox.send_message_and_wait_for_reply(Message(data)).body


# ======================================================================================================================

class EngineResource(BaseResource):

    __slots__ = ()

    # ------------------------------------------------------------------------------------------------------------------

    def on_post(self, req, resp):
        data = CommandPacket.from_dict(req.media).to_dict()
        try:
            out = self._send_to_engine(data)
            data_out = json.loads(out)
            if not data_out['ok']:
                resp.status = falcon.HTTP_500
            resp.media = data_out
        except TimeoutException:
            resp.status = falcon.HTTP_500
            resp.media = dict(timeout=True)


    # ------------------------------------------------------------------------------------------------------------------


    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = 'ok'

# ======================================================================================================================

class IndexResource(object):

    __slots__ = ('path',)

    def __init__(self, path=None):
        self.path = path

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        filename = os.path.join(self.path, 'index.html')
        with open(filename, 'r') as f:
            resp.body = f.read()

# ======================================================================================================================

class PagesResource(BaseResource):

    __slots__ = ('templar', 'pages')

    def __init__(self, templar=None, mailbox=None):
        self.templar = templar
        super().__init__(mailbox=mailbox)
        self.pages = PageBuilder(templar=templar, mailbox=mailbox)

    def on_get(self, req, resp, category, item):
        resp.status = falcon.HTTP_200
        resp.body = self.pages.render(category, item)

# ======================================================================================================================

def run_server(host='127.0.0.1', port=8000, to_engine=None, to_server=None):

    app = falcon.API()

    mailbox = Mailbox(receive_queue=to_server, send_queue=to_engine)

    p = os.path.abspath(sys.modules[WarpApi.__module__].__file__)
    p = os.path.dirname(os.path.dirname(p))

    static_path = os.path.join(p, 'static')
    template_path = os.path.join(p, 'templates')
    templar = Templar(template_path)

    app.add_route('/', IndexResource(static_path))
    app.add_route('/engine', EngineResource(mailbox=mailbox))
    app.add_route('/pages/{category}/{item}', PagesResource(templar=templar, mailbox=mailbox))
    app.add_static_route('/static', static_path)

    print("ready at http://%s:%s/" % (host, port))

    try:
        httpd = simple_server.make_server(host, port, app)
    except OSError as oe:
        if oe.errno == 48:
            sys.stderr.write("\n\naddress is already in use\n\n")
        raise

    httpd.serve_forever()


