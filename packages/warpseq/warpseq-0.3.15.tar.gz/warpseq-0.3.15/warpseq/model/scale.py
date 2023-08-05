# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# logic behind scale math, allowing for computing of intervals within
# a scale.

from .base import NewReferenceObject
from .note import Note

SCALE_TYPES = dict(
   major              = [ 1, 2, 3, 4, 5, 6, 7 ],
   pentatonic         = [ 1, 2, 3, 5, 6 ],
   pentatonic_minor   = [ 1, 3, 4, 5, 7 ],
   natural_minor      = [ 1, 2, 'b3', 4, 5, 'b6', 'b7' ],
   blues              = [ 1, 'b3', 4, 'b5', 5, 'b7' ],
   dorian             = [ 1, 2, 'b3', 4, 5, 6, 'b7' ],
   chromatic          = [ 1, 'b2', 2, 'b3', 3, 4, 'b5', 5, 'b6', 6, 'b7', 7 ],
   harmonic_major     = [ 1, 2, 3, 4, 5, 'b6', 7 ],
   harmonic_minor     = [ 1, 2, 3, 4, 5, 'b6', 7 ],
   locrian            = [ 1, 'b2', 'b3', 4, 'b5', 'b6', 'b7' ],
   lydian             = [ 1, 2, 3, 'b5', 5, 6, 7 ],
   major_pentatonic   = [ 1, 2, 3, 5, 6 ],
   melodic_minor_asc  = [ 1, 2, 'b3', 4, 5, 'b7', 'b8', 8 ],
   melodic_minor_desc = [ 1, 2, 'b3', 4, 5, 'b6', 'b7', 8 ],
   minor_pentatonic   = [ 1, 'b3', 4, 5, 'b7' ],
   mixolydian         = [ 1, 2, 3, 4, 5, 6, 'b7' ],
   phrygian           = [ 1, 'b2', 'b3', 4, 5, 'b6', 'b7' ],
   japanese           = [ 1, 2, 4, 5, 6 ],
   akebono            = [ 1, 2, 'b3', 5, 6 ]
)

SCALE_TYPE_NAMES = [ k for k in SCALE_TYPES.keys() ]

SCALE_ALIASES = dict(
   aeolian = 'natural_minor',
   ionian = 'major',
   minor = 'natural_minor'
)

def scale_types():
    values = [ x for x in SCALE_TYPES.keys() ]
    return values

class Scale(NewReferenceObject):

    __slots__ = ['name', 'root', 'scale_type', 'slots', '_cached', '_cached_numbers', 'obj_id']

    SAVE_AS_REFERENCES = [ ]

    def __init__(self, name=None, root=None, scale_type=None, slots=None, obj_id=None):
        self.name = name
        self.root = root
        self.scale_type = scale_type
        self.slots = slots
        self.obj_id = obj_id
        self._cached = None
        super(Scale, self).__init__()
        if self.root:
            self._internal_generate()

    def post_load(self):
        print("B")
        self._internal_generate()

    def get_notes(self):
        return self._cached

    def get_first(self):
        return self._cached[0]

    def get_note_numbers(self):
        return self._cached_numbers

    def save_root(self):
        return [ self.root.name, self.root.octave ]

    def load_root(self, song, data):
        return Note(name=data[0], octave=data[1])

    def _internal_generate(self, length=120):


        """
        Allows traversal of a scale in a forward direction.
        Example:
        for note in scale.generate(length=7):
           print(note)
        """

        scale_data = self.slots

        if not scale_data:
            scale_type = SCALE_ALIASES.get(self.scale_type, self.scale_type)
            scale_data = SCALE_TYPES[scale_type][:]

        octave_shift = 0
        index = 0

        cache = []

        while (length is None or length > 0):

            if index >= len(scale_data):
               index = 0
               octave_shift = octave_shift + 1

            try:
                result = self.root.copy().transpose(degrees=scale_data[index], octaves=octave_shift)
                #print("res=%s" % result)
            except IndexError:
                return

            cache.append(result)

            index = index + 1
            if length is not None:
                length = length - 1

        self._cached = cache
        self._cached_numbers = [ x.note_number() for x in self._cached ]
