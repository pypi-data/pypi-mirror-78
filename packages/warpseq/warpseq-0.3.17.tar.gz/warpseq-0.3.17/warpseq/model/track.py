# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a track is a vertical row of clips that share a common instrument.
# a track can also be muted.

from .base import NewReferenceObject
from .instrument import Instrument
from warpseq.utils import utils

ALL_INSTRUMENTS = 'all_instruments'
ROTATE = 'rotate'
ROTATE_CHORDS = 'rotate_chords'
SPREAD = 'spread'
INSTRUMENT_MODE_CHOICES = [ ALL_INSTRUMENTS, ROTATE, ROTATE_CHORDS, SPREAD ]

class Track(NewReferenceObject):

    __slots__ = [ 'name', 'muted', 'instruments', 'clip_ids', 'obj_id', 'instrument_mode', '_all_instruments', '_hocket_roller', 'hidden' ]

    SAVE_AS_REFERENCES = [ 'instruments' ]

    def __init__(self, name=None, muted=False, instrument=None, instruments=None, instrument_mode=ALL_INSTRUMENTS, clip_ids=None, obj_id=None, hidden=None):

        self.name = name
        self.muted = muted
        self.hidden = hidden
        self.obj_id = obj_id

        if not instruments and instrument:
            instruments = [ instrument ]
        if instruments is None:
            instruments = []

        self.instruments = instruments

        if instrument_mode is None:
            instrument_mode = ALL_INSTRUMENTS

        self.instrument_mode = instrument_mode

        assert instrument_mode in INSTRUMENT_MODE_CHOICES

        if clip_ids is None:
            clip_ids = []
        self.clip_ids = clip_ids

        self._hocket_roller = utils.roller(self.instruments)

        super(Track, self).__init__()


    # ------------------------------------------------------------------------------------------------------------------

    def get_instruments(self, evt, chosen, instrument_mode):
        if instrument_mode == ALL_INSTRUMENTS:
            return self.instruments
        elif instrument_mode in [ROTATE_CHORDS, SPREAD]:
            return [next(self._hocket_roller)]
        elif instrument_mode == ROTATE:
            return [chosen]
        else:
            raise Exception("unknown mode")

    # ------------------------------------------------------------------------------------------------------------------

    def before_instrument_select(self, instrument_mode):

        if instrument_mode == SPREAD:
            self._hocket_roller = utils.roller(self.instruments)
        if instrument_mode == ROTATE:
            return next(self._hocket_roller)
        return None

    # ------------------------------------------------------------------------------------------------------------------

    def has_clip(self, clip):
        return clip.obj_id in self.clip_ids

    def add_clip(self, clip):
        if clip.obj_id not in self.clip_ids:
            self.clip_ids.append(clip.obj_id)

    def remove_clip(self, clip):
        self.clip_ids = [ c for c in self.clip_ids if c != clip.obj_id ]

    def is_hidden(self):
        return self.hidden