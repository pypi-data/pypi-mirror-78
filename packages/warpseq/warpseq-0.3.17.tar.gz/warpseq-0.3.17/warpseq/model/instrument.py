# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# an instrument adds a channel number to a MIDI device and has some
# parameters around supported note ranges. It can also be muted.

from .base import NewReferenceObject
import functools

class Instrument(NewReferenceObject):

    __slots__ = [ 'name', 'channel', 'device', 'min_octave', 'base_octave', 'max_octave', 'default_velocity', 'muted' ]

    SAVE_AS_REFERENCES = [ 'device' ]

    def __init__(self, name=None, channel=1, device=None, min_octave=0, base_octave=3, max_octave=10,
                 default_velocity=120, muted=False, obj_id=None):

        self.name = name

        if channel is not None:
            channel = int(channel)

        self.channel = channel
        self.device = device
        self.min_octave = min_octave
        self.base_octave = base_octave
        self.max_octave = max_octave
        self.default_velocity = default_velocity
        self.muted = muted
        self.obj_id = obj_id

        super(Instrument,self).__init__()

    @functools.lru_cache()
    def get_midi_out(self):
        return self.device.get_midi_out()
