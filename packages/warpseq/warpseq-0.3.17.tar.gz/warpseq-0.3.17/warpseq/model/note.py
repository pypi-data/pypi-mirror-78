# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from ..api.exceptions import *
from . note_table import NOTE_TABLE
from warpseq.utils import utils

DEFAULT_VELOCITY = 120

NOTES          = [ 'C',  'Db', 'D', 'Eb', 'E',  'F',  'Gb', 'G',  'Ab', 'A', 'Bb', 'B' ]
EQUIVALENCE    = [ 'C',  'C#', 'D', 'D#', 'E',  'F',  'F#', 'G',  'G#', 'A', 'A#', 'B' ]
EQUIVALENCE_SET = set(EQUIVALENCE)

SCALE_DEGREES_TO_STEPS = {
   '0'  : 0, # just to ignore extraneous input
   '1'  : 0, # C (if C major)
   'b2' : 0.5,
   '2'  : 1, # D
   'b3' : 1.5,
   '3'  : 2, # E
   '4'  : 2.5, # F
   'b5' : 3,
   '5'  : 3.5, # G
   'b6' : 4,
   '6'  : 4.5, # A
   'b7' : 5,
   '7'  : 5.5, # B
   '8'  : 6
}

SCALE_DEGREES_FOR_UI = [x for x in  SCALE_DEGREES_TO_STEPS.keys() if x != '0' ]

class Note(object):

    __slots__ = ( 'name', 'octave', 'tie', 'length', 'start_time', 'end_time', 'velocity', 'from_scale',
                  'from_parser', 'repeat', 'length_mod', 'tied', 'delay', 'no_shift', 'muted', 'track_copy',
                  'ccs', 'deferred_expressions', 'from_context', 'octave_set_recorded', 'octave_shifts_recorded', 'degree_shifts_recorded')

    SAVE_AS_REFERENCES = []

    def __init__(self, name=None, octave=0, tie=False, length=None, start_time=None, end_time=None,
                 velocity=DEFAULT_VELOCITY, from_scale=None, from_parser=None, repeat=None, length_mod=1, tied=0, delay=0,
                 no_shift=False, muted=False, track_copy=None, ccs=None, deferred_expressions=None,
                 from_context=None, octave_set_recorded=None, octave_shifts_recorded=0, degree_shifts_recorded=0):

         if name in EQUIVALENCE_SET:
             name = NOTES[EQUIVALENCE.index(name)]
         self.name = name

         self.octave = octave
         self.tie = tie
         self.length = length
         self.start_time = start_time
         self.end_time = end_time
         self.velocity = velocity
         self.from_scale = from_scale
         self.from_parser = from_parser
         self.repeat = repeat
         self.length_mod = length_mod
         self.no_shift = no_shift
         self.tied = tied
         self.delay = delay
         self.muted = muted
         self.from_context = from_context
         # needed to process deferred track grabs
         self.octave_set_recorded = octave_set_recorded
         self.octave_shifts_recorded = octave_shifts_recorded
         self.degree_shifts_recorded = degree_shifts_recorded

         if ccs is None:
             ccs = {}
         if deferred_expressions is None:
             deferred_expressions = []
         self.ccs = ccs
         self.deferred_expressions = deferred_expressions

         if track_copy is None:
             track_copy = []
         self.track_copy = track_copy

    def to_dict(self):
        # this is only used by serializing the scale root
        return dict(name=self.name, octave=self.octave)

    @classmethod
    def from_dict(self, data):
        # this is only used by deserializing the scale root
        return Note(name=data['name'], octave=data['octave'])

    def copy(self):
        """
        Returns a new Note with the same data as the current Note
        """
        return Note(name=self.name,
                    octave=self.octave,
                    tie=self.tie,
                    length=self.length,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    velocity=self.velocity,
                    from_scale=self.from_scale,
                    from_parser=self.from_parser,
                    repeat = self.repeat,
                    length_mod = self.length_mod,
                    tied = self.tied,
                    delay = self.delay,
                    no_shift = self.no_shift,
                    muted = self.muted,
                    track_copy = self.track_copy[:],
                    ccs = self.ccs,
                    deferred_expressions = self.deferred_expressions[:],
                    from_context = self.from_context,
                    octave_shifts_recorded = self.octave_shifts_recorded,
                    degree_shifts_recorded = self.degree_shifts_recorded,
                    octave_set_recorded = self.octave_set_recorded
        )

    def get_parser(self):
        return self.from_parser

    def chordify(self, chord_type):
        from . chord import Chord
        return Chord(root=self, chord_type=chord_type, from_scale=self.from_scale)

    def scale_transpose(self, scale_obj, steps):

        snn = self.note_number()
        scale_notes = scale_obj.get_notes()
        note_numbers = scale_obj.get_note_numbers()

        new_index = utils.index_where_exceeds(note_numbers, snn) + steps

        if new_index < 0:
            correct_octaves = (int(new_index / 12) * -1) + 1
            return self.transpose(octaves=correct_octaves).scale_transpose(scale_obj, steps).transpose(octaves=-correct_octaves)

        scale_note = scale_notes[new_index ]
        n1 = self
        n1.name = scale_note.name
        n1.octave = scale_note.octave
        n1.from_scale = scale_obj
        return n1

    def tie_count(self):
        # how many milliseconds should we add from ties marked after this note?
        return self.tied

    def record_octave_set(self, value):
        self.octave_set_recorded = value
        self.octave_shifts_recorded = 0

    def record_octave_shift(self, value):
        self.octave_shifts_recorded = self.octave_shifts_recorded + value

    def record_degree_shift(self, value):
        self.degree_shifts_recorded = self.degree_shifts_recorded + value

    def with_tied(self, amount):
        self.tied = amount
        return self

    def shiftable(self):
        return not self.no_shift

    def get_track_copy(self):
        return self.track_copy

    def is_muted(self):
        return self.muted

    def with_velocity(self, velocity):
        n1 = self
        n1.velocity = velocity
        return n1

    def with_muted(self, muted):
        n1 = self
        n1.muted = muted
        return n1

    def with_track_copy(self, track):
        n1 = self
        if track not in n1.track_copy:
            n1.track_copy.append(track)
        return n1

    def with_repeat(self, repeat):
        n1 = self
        n1.repeat = repeat
        return n1

    def with_no_shift(self):
        n1 = self
        n1.no_shift = True
        return n1

    def with_delay(self, delay):
        n1 = self
        n1.delay = delay
        return n1

    def with_octave(self, octave):
        n1 = self
        n1.octave = octave
        return n1

    def with_length_mod(self, mod):
        n1 = self
        n1.length_mod = mod
        return n1

    def replace_with_note(self, name, octave):
        n1 = self
        n1.name = name
        n1.octave = octave
        return n1

    def with_cc(self, channel, value):
        n1 = self
        n1.ccs[str(channel)] = value
        return n1

    def with_timing(self, start_time=None, end_time=None, length=None):
        n1 = self
        n1.start_time = start_time
        n1.end_time = end_time
        n1.length = length
        return n1

    def transpose(self, steps=0, semitones=0, degrees=0, octaves=0):
        # FIXME: improve to not use the note table?

        degree_steps = SCALE_DEGREES_TO_STEPS[str(degrees)]
        steps = steps + (semitones * 0.5) + degree_steps

        result = self
        if steps:
            new_index = result.note_number() + int(2*steps) + 60
            if new_index < 0:
                raise InvalidNote("negative note range exceeded")
            (result.name, result.octave) = NOTE_TABLE[new_index]
        if octaves:
            result.octave = result.octave + octaves
        return result

    def get_notes(self):
        return [ self ]

    def note_number(self):
        return NOTES.index(self.name) + (12 * self.octave)

    def invert(self, *args):
        return self

    def with_name(self, name):
        n1 = self
        n1.name = name
        return n1

    def __repr__(self):
        # FIXME: this will be simplified once we are doing less note debugging
        return "Note<%s|%s,len=%s,time=%s/%s,cc=%s,tie=%s,muted=%s,track_copy=%s,def=%s,tied=%s>" % (
            self.name,
            self.octave,
            self.length,
            self.start_time,
            self.end_time,
            self.ccs,
            self.tie,
            self.muted,
            [x.name for x in self.track_copy],
            self.deferred_expressions,
            self.tied
        )

