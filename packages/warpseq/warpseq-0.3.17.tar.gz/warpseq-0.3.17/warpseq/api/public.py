# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this implements the public Python API for WarpSeq.
# see examples/api/*.py for usage

import gc
import random
import json

from warpseq.api.interfaces.devices import Devices
from warpseq.api.interfaces.instruments import Instruments
from warpseq.api.interfaces.patterns import Patterns
from warpseq.api.interfaces.transforms import Transforms
from warpseq.api.interfaces.player import Player
from warpseq.api.interfaces.scales import Scales
from warpseq.api.interfaces.scenes import Scenes
from warpseq.api.interfaces.song import SongApi
from warpseq.api.interfaces.tracks import Tracks
from warpseq.api.interfaces.clips import Clips
from warpseq.api.interfaces.data_pools import DataPools
from warpseq.playback import midi
from warpseq.model.song import Song
from warpseq.api.callbacks import Callbacks, DefaultCallbacks

gc.disable()
MIDI_PORTS = midi.get_devices()

class Api(object):

    __slots__ = ( '_song', 'song', 'devices', 'instruments', 'scales',
                  'patterns', 'data_pools', 'transforms', 'scenes', 'tracks', 'clips',
                  'player', 'song', '_callbacks' )

    def __init__(self, default_callbacks=True):
        self._reset()
        self._callbacks = Callbacks()
        if default_callbacks:
            self._callbacks.clear()
            self._callbacks.register(DefaultCallbacks())

    def remove_callbacks(self):
        self._callbacks.clear()

    def add_callbacks(self, cb):
        self._callbacks.register(cb)

    def _reset(self):

        self._song = Song(name='')
        self._setup_api()

    def _setup_api(self):
        self.song = SongApi(self, self._song)
        self.devices = Devices(self, self._song)
        self.instruments = Instruments(self, self._song)
        self.scales  = Scales(self, self._song)
        self.patterns = Patterns(self, self._song)
        self.data_pools = DataPools(self, self._song)
        self.transforms = Transforms(self, self._song)
        self.scenes = Scenes(self, self._song)
        self.tracks = Tracks(self, self._song)
        self.clips = Clips(self, self._song)
        self.player = Player(self, self._song)

        random.seed()

    # ------------------------------------------------------------------------------------------------------------------
    # FIXME: song save/load work in progress

    def reset(self):
        self._reset()
        self.scales.add(name='C-major', note='C', octave=0, scale_type='major')
        for x in range(1,5):
            self.scenes.add(name='Scene %s' % x)
            self.tracks.add(name='Track %s' % x, instruments=[])

    def from_dict(self, data):
        self._song = Song.from_dict(data)
        self._setup_api()

    def to_dict(self):
        return self._song.to_dict()

    def from_json(self,  data):
        data = json.loads(data)
        return self.from_dict(data)

    def to_json(self):
        return self._song.to_json()

    def load(self, filename:str):
        fh = open(filename, "r")
        data = fh.read()
        fh.close()
        self.from_json(data)
        self._song.filename = filename


    def save(self):
        if not self._song.filename:
            raise InvalidUsage("no filename set, use save_as")
        data = self._song.to_json()
        fh = open(self._song.filename, "w+")
        fh.write(data)
        fh.close()

    def save_as(self, filename:str):
        self._song.filename = filename
        self.save()
