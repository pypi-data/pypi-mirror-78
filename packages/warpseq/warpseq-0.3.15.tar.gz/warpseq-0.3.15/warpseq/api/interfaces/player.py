# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.playback.realtime_engine import RealtimeEngine
from warpseq.playback.multi_player import MultiPlayer
from warpseq.api.exceptions import AllClipsDone, WarpException
import sys
import traceback

class Player(object):

    def __init__(self, public_api, song):
        self.public_api = public_api
        self.song = song
        self.multi_player = MultiPlayer(song=song, engine_class=RealtimeEngine)

    def play_scene(self, scene):
        scene = self.public_api.scenes.lookup(scene, require=True)
        self.multi_player.play_scene(scene)

    def play_clips(self, clips):
        clips = [ c for c in self.public_api.clips.lookup(c, require=True) ]
        self.multi_player.add_clips(clips)

    def stop_clips(self, clips):
        clips = [ c for c in self.public_api.clips.lookup(c, require=True) ]
        for c in clips:
            self.multi_player.remove_clip(c)

    def stop(self):
        self.multi_player.stop()

    def advance(self):
        self.multi_player.advance()

    def loop(self, scene_name, abort=True, stop_if_empty=True, infinite=False):

        while True:

            self.multi_player.stop_if_empty = stop_if_empty
            self.play_scene(scene_name)

            try:
                while True:
                    self.advance()
            except KeyboardInterrupt:
                self.public_api._callbacks.keyboard_interrupt()
                self.stop()
                if abort:
                    sys.exit(0)
            except AllClipsDone:
                self.public_api._callbacks.all_clips_done()
            except WarpException:
                traceback.print_exc()
                try:
                    self.stop()
                except:
                    pass
                if abort:
                    sys.exit(0)
                else:
                    raise

            if not infinite:
                break

