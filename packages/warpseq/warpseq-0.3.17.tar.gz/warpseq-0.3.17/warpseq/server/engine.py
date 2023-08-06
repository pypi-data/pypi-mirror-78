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
import json

class WarpBackgroundEngine(object):

    __slots__ = ('_api', '_mailbox', '_api_router', 'debug', 'callbacks', '_startup_reply' )

    def __init__(self, mailbox=None):

        self._api = WarpApi()
        self._api.reset()
        self._api_router = ApiRouter(self._api, self)
        self._mailbox = mailbox
        mailbox.source = 'main_process'
        self.callbacks = EngineCallbacks(engine=self)
        self._api_router.callbacks = self.callbacks
        self._startup_reply = None


        self.debug = False

        api = WarpApi()
        api.remove_callbacks()
        api.add_callbacks(self.callbacks)
        api.song.edit(tempo=120)

        self._api = api

    def _reply(self, msg, data):
        self._mailbox.send_reply(msg, Message(body=data))

    def check_messages(self):

        messages = self._mailbox.get_unexpected_messages()

        for msg in messages:

            command_packet = CommandPacket.from_dict(msg.body)
            response_packet = self._api_router.dispatch(msg, command_packet)
            if response_packet:
                # play commands don't return none here, they have to return inside
                # the event loop
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
            engine._mailbox.source = "main_process"

            # FIXME: we'll probably not need this logic anymore.
            # print("return from engine...")
            #if engine._startup_reply:
            #    print("GOT STARTUP REPLY")
            #    # if we exit the engine we need to respond to any messages when we get back
            #    engine._reply(engine._startup_reply, json.dumps(dict(ok=True)))
            #    engine._startup_reply = None

        except KeyboardInterrupt:

            return



