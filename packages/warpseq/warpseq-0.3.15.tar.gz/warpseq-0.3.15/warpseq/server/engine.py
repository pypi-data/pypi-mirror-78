# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.server.mailbox import Mailbox, Message
from warpseq.api.public import Api as WarpApi
from warpseq.server.callbacks import EngineCallbacks
from warpseq.server.packet import CommandPacket
from warpseq.server.api_router import ApiRouter
import sys
import time

class WarpBackgroundEngine(object):

    __slots__ = ('_api', '_mailbox', '_api_router' )

    def __init__(self, mailbox=None):

        self._api = WarpApi()
        self._api.reset()
        self._api_router = ApiRouter(self._api)
        self._mailbox = mailbox

        api = WarpApi()
        api.remove_callbacks()
        api.add_callbacks(EngineCallbacks(engine=self))
        api.song.edit(tempo=120)

        self._api = api

    def _reply(self, msg, data):
        self._mailbox.send_reply(msg, Message(body=data))

    def check_messages(self):

        found = False

        messages = self._mailbox.get_unexpected_messages()

        for msg in messages:

            found = True

            command_packet = CommandPacket.from_dict(msg.body)
            response_packet = self._api_router.dispatch(command_packet)
            response_data = response_packet.to_json()

            self._reply(msg, response_data)


def run_engine(to_engine=None, to_server=None):


    mailbox = Mailbox(receive_queue=to_engine, send_queue=to_server)
    engine = WarpBackgroundEngine(mailbox=mailbox)

    while True:

        try:

            # ask the engine to do things here - including start the event loop
            # when inside the event loop the engine must be able to call this same
            # handler from a callback

            engine.check_messages()
            time.sleep(0.001)

        except KeyboardInterrupt:

            return



