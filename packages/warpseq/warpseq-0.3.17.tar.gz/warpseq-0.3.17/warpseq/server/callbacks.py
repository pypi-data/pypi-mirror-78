# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.api.callbacks import BaseCallbacks
from warpseq.server.packet import ResponsePacket
from warpseq.api.exceptions import StopException
import json

class EngineCallbacks(BaseCallbacks):

    __slots__ = ('engine','mailbox','startup_reply')

    def __init__(self, engine=None):
        self.engine = engine
        self.startup_reply = None

    def on_scene_start(self, scene):

        print("ON_SCENE_START")

        self.engine._mailbox.source = "event_loop"

        if self.startup_reply:
            print("WE HAVE A STARTUP REPLY!")
            # we have to send the event that says we started up, else the web server is going to timeout
            self.engine._reply(self.startup_reply, json.dumps(dict(ok=True)))
            self.startup_reply = None

        self._handle_messages();

    def on_clip_start(self, clip):
        print(">> starting clip: %s (%s)" % (clip.name, clip.obj_id))

    def on_clip_stop(self, clip):
        print(">> stopping clip: %s (%s)" % (clip.name, clip.obj_id))

    def on_clip_restart(self, clip):
        print(">> restarting clip: %s (%s)" % (clip.name, clip.obj_id))

    def on_pattern_start(self, clip, pattern):
        print(">> starting pattern: %s (%s)/%s (%s)" % (clip.name, clip.obj_id, pattern.name, pattern.obj_id))

    def all_clips_done(self):
        print(">> all clips done")

    def keyboard_interrupt(self):
        print(">> keyboard interrupt")

    def on_multiplayer_advance(self):
        self._handle_messages()

    def _handle_messages(self):

        try:
            self.engine.check_messages()
        except StopException:
            self.engine._api.player.stop()
            raise AllClipsDone()
