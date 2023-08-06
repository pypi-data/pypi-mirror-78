# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# https://en.wikipedia.org/wiki/Chord_names_and_symbols_(popular_music)
# minor 2nd - 2 semitones
# minor 3rd - 3 semitones
# major 3rd - 4 semitones
# perfect 4th - 5 semitones
# perfect 5th - 7 semitones
# major 6th - 9 semitones
# major 7th - 11 semitones
# octave - 12 semitones
# etc

CHORD_TYPES = dict(
   minor = ( 3, 7 ),
   major = ( 4, 7 ),
   dim = ( 3, 6 ),
   aug = ( 4, 8 ),
   sus4 = ( 5, 7 ),
   sus2 = ( 2, 7 ),
   fourth = ( 5, ),
   power = ( 7, ),
   fifth = ( 7, ),
   M6 = ( 4, 7, 9 ),
   m6 = ( 3, 7, 9 ),
   dom7 = ( 4, 7, 10 ),
   M7 = ( 4, 7, 11 ),
   m7 = ( 3, 7, 10 ),
   aug7 = ( 4, 8, 10 ),
   dim7 = ( 3, 6, 10 ),
   mM7 = ( 3, 7, 11 )
)

CHORD_TYPE_KEYS = set([x for x in CHORD_TYPES.keys()])


class Chord(object):

    __slots__ = ( "notes", "root", "chord_type", "from_scale", "length", "deferred_expressions" )

    def __init__(self, notes=None, root=None, chord_type=None, from_scale=None, deferred_expressions=None):

        self.notes = notes
        self.root = root
        self.chord_type = chord_type
        self.from_scale = from_scale
        if deferred_expressions is None:
            deferred_expressions = []
        self.deferred_expressions = deferred_expressions

        # chord length is meaningless, this just makes some code not have to do a type check
        self.length = None


        if self.notes is None:
            offsets = CHORD_TYPES[self.chord_type]
            notes = [root.copy()]
            notes.extend([root.copy().transpose(semitones=offset) for offset in offsets])
            self.notes = notes

    def shiftable(self):
        return False not in [ x.shiftable() for x in self.notes ]

    def chordify(self, chord_type):
        return Chord(root=self.notes[0].copy(), chord_type=chord_type, from_scale=self.notes[0].from_scale)

    def copy(self):
        return Chord(notes=self.notes, from_scale=self.from_scale)

    def with_notes(self, new_notes):
        return Chord(notes=new_notes, from_scale=self.from_scale)

    def with_velocity(self, velocity):
        return self.with_notes([x.with_velocity(velocity) for x in self.notes])

    def with_repeat(self, repeat):
        return self.with_notes([x.with_repeat(repeat) for x in self.notes])

    def with_length_mod(self, mod):
        return self.with_notes([x.with_length_mod(mod) for x in self.notes])

    def tie_count(self):
        if len(self.notes):
            return self.notes[0].tie_count()
        return 0

    def with_tied(self, amount):
        return self.with_notes([x.with_tied(amount) for x in self.notes])

    def with_delay(self, delay):
        return self.with_notes([x.with_delay(mod) for x in self.notes])

    def with_cc(self, channel, num):
        return self.with_notes([ x.with_cc(channel, num) for x in self.notes ])

    def with_muted(self, muted):
        return self.with_notes([ x.with_muted(muted) for x in self.notes ])

    def is_muted(self):
        return True in [ x.muted for x in self.notes ]

    def get_track_copy(self):
        if not len(self.notes):
            return False
        return self.notes[0].get_track_copy()

    def with_track_copy(self, track):
        return self.with_notes([ x.with_track_copy(track) for x in self.notes ])

    def replace_with_note(self, name, octave):
        return self.with_notes([ self.notes[0].replace_with_note(name,octave) ])

    def with_octave(self, octave):
        if not self.notes:
            return self.copy()
        delta = octave - self.notes[0].octave
        return self.with_notes([ n.with_octave(n.octave+delta) for n in self.notes ])

    def with_timing(self, start_time=None, end_time=None, length=None):
        return self.with_notes([ x.with_timing(start_time=start_time, end_time=end_time, length=length) for x in self.notes ])

    def scale_transpose(self, scale_obj, steps):
        return self.with_notes([ x.copy().scale_transpose(scale_obj, steps) for x in self.notes ])

    def transpose(self, steps=0, semitones=0, octaves=0):
        return self.with_notes([ note.copy().transpose(steps=steps, octaves=octaves, semitones=semitones) for note in self.notes ])

    def invert(self, amount=1, octaves=1):
        new_chord = self.copy()
        if amount >= 1:
            new_chord.notes[0] = new_chord.notes[0].transpose(octaves=octaves)
        if amount >= 2:
            new_chord.notes[1] = new_chord.notes[1].transpose(octaves=octaves)
        if amount >= 3:
            new_chord.notes[2] = new_chord.notes[2].transpose(octaves=octaves)
        return new_chord

    def get_parser(self):
        return self.notes[0].get_parser()

    def get_notes(self):
        return self.notes

    def record_octave_set(self, value):
        for x in self.notes:
            note.record_octave_set(value)

    def record_octave_shift(self, value):
        for x in self.notes:
            x.record_octave_shift(value)

    def record_degree_shift(self, value):
        for x in self.notes:
            note.record_degree_set(value)

    def __repr__(self):
        return "Chord <%s>" % (",".join(str(x) for x in self.notes))
