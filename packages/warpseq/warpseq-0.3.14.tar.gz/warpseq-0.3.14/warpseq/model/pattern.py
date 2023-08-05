# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a Pattern is a list of symbols/expressions that will eventually
# evaluate into Chords/Notes.

from .base import NewReferenceObject
from warpseq.api.exceptions import *
from warpseq.model.directions import *
from warpseq.model.slot import Slot

class Pattern(NewReferenceObject, Directionable):

    __slots__ = [ 'name', 'slots', '_current_slots', 'octave_shift', 'rate', 'scale', 'direction', '_current_direction',
                  'length', '_iterator', 'obj_id' ]

    SAVE_AS_REFERENCES = [ 'scale' ]

    def __init__(self, name=None, slots=None, octave_shift=0, rate=1, scale=None, direction=FORWARD, length=None,
                 obj_id=None):

        self.name = name
        self.slots = slots

        self.octave_shift = octave_shift
        self.rate = rate
        self.scale = scale

        for x in slots:
            assert isinstance(x, Slot)

        if length is None:
            length = len(slots)

        self.length = length

        if not direction in DIRECTIONS:
            raise InvalidInput("direction must be one of: %s" % DIRECTIONS)

        self.direction = direction
        self._current_direction = direction
        self.obj_id = obj_id

        super(Pattern, self).__init__()
        self.reset()

    def get_octave_shift(self, track):
        return self.octave_shift

    def get_length(self):
        return self.length

    def get_iterator(self):
        for _ in range(0, self.get_length()):
            yield next(self._iterator)
