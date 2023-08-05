# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

import time
from warpseq.api.exceptions import TimeoutException
from multiprocessing.queues import Empty

SLEEP_AMOUNT = 0.001
TIMEOUT = 10
NEXT_MESSAGE_ID = 0

# ======================================================================================================================

class Message(object):

    __slots__ = ('msg_id', 'body', 'reply_to_id')

    def __init__(self, body=None, msg_id=None, reply_to_id=None):
        self.body = body
        self.msg_id = msg_id
        self.reply_to_id = reply_to_id

        if msg_id is None:
            self.msg_id = self._get_next_message_id()

    # ------------------------------------------------------------------------------------------------------------------

    def _get_next_message_id(self):

        global NEXT_MESSAGE_ID
        NEXT_MESSAGE_ID = NEXT_MESSAGE_ID + 1
        if NEXT_MESSAGE_ID > 10000:
            NEXT_MESSAGE_ID = 0
        return NEXT_MESSAGE_ID

# ======================================================================================================================

class Mailbox(object):

    __slots__ = ('send_queue', 'receive_queue', 'incoming_data', 'response_data')

    def __init__(self, send_queue=None, receive_queue=None):

        self.send_queue = send_queue
        self.receive_queue = receive_queue
        self.incoming_data = []
        self.response_data = {}

    # ------------------------------------------------------------------------------------------------------------------

    def _wait_for_reply(self, msg_id, spin=SLEEP_AMOUNT, timeout=TIMEOUT):
        """ Wait for a given reply to earlier message to come in, and then return the reply """

        t1 = time.perf_counter() + timeout

        while True:

            if msg_id in self.response_data:
                msg = self.response_data[msg_id]
                del self.response_data[msg_id]
                return msg

            t2 = time.perf_counter()

            self._post_office_receive_all_messages()

            if t2 > t1:
                raise TimeoutException()

            time.sleep(spin)

    # ------------------------------------------------------------------------------------------------------------------

    def get_unexpected_messages(self):
        """ Get all messages that were not replies to messages """

        self._post_office_receive_all_messages()

        results = []

        while True:
            try:
                item = self.incoming_data.pop()
            except IndexError:
                return results

            results.append(item)

    # ------------------------------------------------------------------------------------------------------------------

    def send_message(self, message):
        """ Send an unsolicited message that is not a reply """
        self.send_queue.put(message)
        return message

    # ------------------------------------------------------------------------------------------------------------------

    def send_reply(self, message, response):
        """ Reply to a message. """
        response.reply_to_id = message.msg_id
        self.send_queue.put(response)
        return response

    # ------------------------------------------------------------------------------------------------------------------

    def send_message_and_wait_for_reply(self, message):
        """ Sends a message and blocks until the reply comes in """
        message = self.send_message(message)
        return self._wait_for_reply(message.msg_id)

    # ------------------------------------------------------------------------------------------------------------------

    def _post_office_receive_all_messages(self):

        while True:
            try:
                obj = self.receive_queue.get(block=False)
            except Empty:
                return

            if obj.reply_to_id is not None:
                self.response_data[obj.msg_id] = obj
            else:
                self.incoming_data.append(obj)

