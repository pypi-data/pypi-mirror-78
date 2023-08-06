# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# the multi-player class contains high level methods for playing
# clips and scenes, as such the individual (track-specific) interface,
# player.py, is a less public API than this one.

import ctypes
import time

from ..api.callbacks import Callbacks
from ..api.exceptions import AllClipsDone
from ..model.base import BaseObject
import time
import gc

LONG_WAIT = 20 / 1000
SHORT_WAIT = 1 / 8000
MILLISECONDS = 2

class MultiPlayer(object):

    __slots__ = [ 'song', 'engine_class', 'clips', 'players', 'callbacks', 'stop_if_empty', 'stopped']

    def __init__(self, song=None, engine_class=None, stop_if_empty=True):
        self.song = song
        self.engine_class = engine_class

        self.clips = []
        self.players = {}
        self.stop_if_empty = stop_if_empty
        self.callbacks = Callbacks()
        self.stopped = False

    def stop(self):
        """
        Stops all clips.
        """

        #self.stopped = True
        # stop all players that are attached
        for (n, p) in self.players.items():
            # this is needed if the players are set to infinite repeat
            # so they won't restart
            p.stopped = True
            # this removes the players
            p.stop()

        # clear the list of things that are playing, in case we start more
        self.clips = []
        self.players = {}

    def advance(self):

        """
        return all events from now to TIME_INTERVAL and then move the time index up by that amount.
        the multiplayer doesn't keep track of the time indexes themselves, the clips do, and they may
        all run at different speeds.
        """
        if self.stopped:
            print("I AM STOPPED")
            return

        self.callbacks.on_multiplayer_advance()

        my_players = [ p for p in self.players.values() ]
        wait_times = [ t for t in [ p2.wait_time() for p2 in [ p for p in my_players if p.has_events() ]] if t > 0 ]

        if len(wait_times) == 0:
            wait_time = MILLISECONDS
        else:
            wait_time = min(wait_times) - MILLISECONDS
            if wait_time < MILLISECONDS:
                wait_time = MILLISECONDS

        for p in my_players:
            p.advance(wait_time)

        desired = time.perf_counter() + (wait_time/1000.0)

        if wait_time > LONG_WAIT:
            time.sleep((wait_time * 0.00095)) # 95 percent of original value, in milliseconds

        while time.perf_counter() < desired:
            time.sleep(SHORT_WAIT)

    def play_scene(self, scene):
        """
        Plays all clips in a scene, first stopping all clips that might be playing elsewhere.
        """
        self.stopped = False
        self.stop()
        self.callbacks.on_scene_start(scene)
        clips = scene.clips(self.song)
        self.add_clips(clips)

    def add_clips(self, clips):
        """
        Adds a clip to be playing by creating a Player for it.
        """

        gc.collect()

        for clip in clips:

            # starts a clip playing, including stopping any already on the same track
            self.callbacks.on_clip_start(clip)

            clip.reset()
            assert clip.track is not None

            need_to_stop = [ c for c in self.clips if clip.track.obj_id == c.track.obj_id ]
            for c in need_to_stop:
                self.remove_clip(c)

            matched = [ c for c in self.clips if c.name == clip.name ]
            if not len(matched):

                self.clips.append(clip)
                player = clip.get_player(self.song, self.engine_class)
                self.players[clip.name] = player
                player._multiplayer = self

        for (k,v) in self.players.items():
            v.start()

    def remove_clip(self, clip, add_pending=False):
        """
        Stops a clip and removes the player for it.
        """

        self.callbacks.on_clip_stop(clip)

        if clip.name in self.players:
            player = self.players[clip.name]
            player.stop()
            del self.players[clip.name]
            self.clips = [ c for c in self.clips if c.name != clip.name ]

        if clip.self_destruct_api_reference:
            clip.self_destruct_api_reference()

        if not add_pending and len(self.clips) == 0 and self.stop_if_empty:
            self.stop()
            raise AllClipsDone()
