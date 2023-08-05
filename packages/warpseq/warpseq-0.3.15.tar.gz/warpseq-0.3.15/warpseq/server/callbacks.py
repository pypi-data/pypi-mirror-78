# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.api.callbacks import BaseCallbacks

class EngineCallbacks(BaseCallbacks):

    __slots__ = ('engine','mailbox',)

    def __init__(self, engine=None):
        self.engine = engine

    def on_scene_start(self, scene):
        self.engine.check_messages()

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
        self.engine.check_messages()