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
from warpseq.parser.web_slots import WebSlotCompiler

STANDARD = 'standard'
PERCUSSION = 'percussion'
PATTERN_TYPES = [ STANDARD, PERCUSSION ]

class Pattern(NewReferenceObject, Directionable):

    __slots__ = [ 'name', 'slots', '_current_slots', 'octave_shift', 'rate', 'scale', 'direction', '_current_direction',
                  'length', '_iterator', 'obj_id', 'audition_with', 'web_slots', 'pattern_type', '_web_slot_compiler' ]

    SAVE_AS_REFERENCES = [ 'scale', 'audition_with' ]

    def __init__(self, name=None, slots=None, octave_shift=0, rate=1, scale=None, direction=FORWARD, length=None,
                 obj_id=None, audition_with=None, web_slots=None, pattern_type=STANDARD):


        # the following is just for testing!

        self.pattern_type = pattern_type
        self._web_slot_compiler =WebSlotCompiler(for_transform=False, pattern_type=self.pattern_type)

        if not slots:
            web_slots = [
                dict(degree=1),
                dict(degree=2),
                dict(degree=3),
                dict(degree=4)
            ]

        self.name = name
        self.slots = slots
        self.set_slots_from_web_slots(web_slots)


        if octave_shift is not None:
            octave_shift = int(octave_shift)
        else:
            octave_shift = 0

        self.octave_shift = octave_shift
        self.rate = rate
        self.scale = scale
        self.audition_with = audition_with

        for x in self.slots:
            assert isinstance(x, Slot)

        if length is None:
            length = len(self.slots)

        self.length = length

        if not direction in DIRECTIONS:
            raise InvalidInput("direction must be one of: %s" % DIRECTIONS)

        self.direction = direction
        self._current_direction = direction
        self.obj_id = obj_id

        super(Pattern, self).__init__()
        self.reset()

    def set_slots_from_web_slots(self, web_slots):

        """
        When deserializing web slots, run the compiler to generate the actual slot objects the engine can run on.
        """

        ok = True
        errors = None
        if web_slots is not None:
            print("WEB SLOTS IS DEFINED")
            (ok, slots, errors) =  self._web_slot_compiler.compile(web_slots)
            if not ok:
                print("WEB SLOTS FAILED")
                self.slots = []
            else:
                print("WEB SLOTS OK!")
                self.slots = slots
        else:
            if self.slots is None:
                self.slots = []
        self.web_slots = web_slots
        if not ok:
            raise Exception("errors during processing: %s" % errors)

    def get_web_slot_grid_for_ui(self, category):
        return self._web_slot_compiler.get_grid(self.web_slots, category)

    def update_web_slots_for_ui(self, data):
        new_web_slots = self._web_slot_compiler.update_web_slots_from_ui(self.web_slots, data)
        self.set_slots_from_web_slots(new_web_slots)

    def get_octave_shift(self, track):
        return self.octave_shift

    def get_length(self):
        return self.length

    def get_iterator(self):
        for _ in range(0, self.get_length()):
            yield next(self._iterator)
