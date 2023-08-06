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
from warpseq.model.slot import Slot, DataSlot

class DataPool(NewReferenceObject, Directionable):

    __slots__ = [ 'name', 'slots', '_current_slots', 'direction', '_current_direction', 'length',
                  '_iterator', 'obj_id' ]

    SAVE_AS_REFERENCES = [ 'slots' ]

    def __init__(self, name=None, slots=None, direction=FORWARD, length=None, obj_id=None):

        # we'll add in web_slots compile soon
        if slots is None:
            slots = []

        self.name = name
        self.slots = slots

        for x in slots:
            assert isinstance(x, DataSlot)

        if not direction in DIRECTIONS:
            raise InvalidInput("direction must be one of: %s" % DIRECTIONS)

        self.direction = direction
        self._current_direction = direction
        self.obj_id = obj_id

        if length is None:
            length = len(slots)
        self.length = length


        super(DataPool, self).__init__()
        self.reset()

