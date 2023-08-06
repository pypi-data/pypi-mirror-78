# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.evaluator import *
from warpseq.model.note import Note
from warpseq.model.registers import get_first_playing_note
import warpseq.utils.serialization as serialization



def evaluate(context=None, subject=None, how=None):
    if isinstance(how, Evaluator):
        res = how.evaluate(context=context, subject=input)
        return evaluate(context=context,  subject=input, how=res)
    return how

class Deferrable(object):

    __slots__ = ('context', 'subject', 'how', 'function')

    def __init__(self, context=None, how=None, function=None):
        self.context = context
        self.how = how
        self.function = function

    def evaluate(self, track, note):
        result = self.function(context=self.context, track=track, subject=note, how=self.how)
        return result

class BaseSlot(object):

    __slots__ = ()

class DataSlot(BaseSlot):

    SAVE_AS_REFERENCES = []

    __slots__ = ('value',)

    def __init__(self, value=None):
        self.value = value

class Slot(BaseSlot):

    SAVE_AS_REFERENCES = []

    __slots__ = ( "note", "octave", "degree", "repeats", "length", "sharp", "flat", "chord_type", "inversion",
        "variables", "track_copy", "track_grab", "rest", "ccs", "delay", "velocity", "skip", "shuffle",
        "reverse", "reset", "tie", "degree_shift", "octave_shift" )

    def __init__(self, note=None, octave=None, octave_shift=None, degree_shift=None, degree=None, repeats=None, length=None, sharp=None, flat=None,
                 chord_type=None, inversion=None, variables=None, track_copy=None, track_grab=None, ccs=None,
                 delay=None, velocity=None, skip=None, shuffle=None, reverse=None, reset=None, tie=None, rest=None):



        self.note = note
        self.octave = octave
        self.degree = degree
        self.repeats = repeats
        self.length = length
        self.sharp = sharp
        self.flat = flat
        self.chord_type = chord_type
        self.inversion = inversion

        self.variables = variables
        self.track_copy = track_copy
        self.ccs = ccs
        self.delay = delay
        self.velocity = velocity
        self.skip = skip
        self.track_grab = track_grab
        self.shuffle = shuffle
        self.reverse = reverse
        self.reset = reset
        self.rest = rest
        self.tie = tie
        self.degree_shift = degree_shift
        self.octave_shift = octave_shift

    def _standardize_input(self, note):

        from warpseq.model.note import Note
        from warpseq.model.chord import Chord

        if type(note) == Chord:
            return note
        elif type(note) == Note:
            return note
        elif type(note) == list:
            if len(note) == 1:
                return note[0]
            else:
                return Chord(notes=note)
        else:
            raise Exception("???")

    # ==================================================================================================================

    def is_hidden(self):
        # needed to appease the serializer
        return False

    # ==================================================================================================================

    def evaluate(self, context, obj):

        # evaluates a Note or Chord or None and always returns a Chord or None

        from warpseq.model.note import Note
        from warpseq.model.chord import Chord

        result = self._compute(context, obj)

        if not result:
            return None
        elif type(result) == Note:
            return Chord(notes=[result])
        return result

    # ==================================================================================================================

    def _compute(self, context, note):

        # FIXME: rename 'note' to 'obj'

        #print("-------")

        note = self._standardize_input(note).copy()

        if note.length is None:
            note.length = context.base_length

        # ----
        # CONTROL FLOW / GLOBAL MANIPULATION / NON-NOTE RELATED OPS

        if self.variables:
            for (k,v) in self.variables.items():
                set_variable(k, evaluate(context=context, subject=note, how=v))

        if self.skip:
            skips = evaluate(context=context, subject=note, how=self.skip)
            for _ in range(0, skips):
                context.pattern.get_next()

        if self.shuffle and evaluate(context=context, subject=note, how=self.shuffle):
            context.pattern.shuffle()

        if self.reverse and evaluate(context=context, subject=note, how=self.reverse):
            context.pattern.reverse()

        if self.reset and evaluate(context=context, subject=note, how=self.reset):
            context.pattern.reset()

        # ----
        # NOTE RELATED OPS THAT DISCARD PITCH

        if evaluate(context=context, subject=note, how=self.tie):
            return Note(tie=True, muted=True)

        if self.rest and evaluate(context=context, subject=note, how=self.rest):
            return None

        # ---
        # NOTE BASICS HERE

        if self.note:
            note = note.with_name(evaluate(context=context, subject=note, how=self.note))
            assert note.length is not None

        if self.degree:
            res = evaluate(context=context, subject=note, how=self.degree) - 1
            # print("debug: set scale scale degree: %s" % res)
            note = note.scale_transpose(context.scale,  res)

        if self.octave is not None:
            res = evaluate(context=context, subject=note, how=self.octave)
            note = note.with_octave(res)
            #print("debug: set octave=%s" % res)
            note.record_octave_set(res)

        # -----
        # NOTE MODIFICATIONS HERE

        if self.octave_shift is not None:
            how = evaluate(context=context, subject=note, how=self.octave_shift)
            note = note.transpose(octaves=how)
            #print("octave transpose: %s" % how)
            note.record_octave_shift(how)

        if self.degree_shift is not None:
            how = evaluate(context=context, subject=note, how=self.degree_shift)
            note = note.scale_transpose(context.scale, how)
            #print("degree shift: %s" % how)
            note.record_degree_shift(how)

        if self.repeats:
            note = note.with_repeat(evaluate(context=context, subject=note, how=self.repeats))

        if self.length and self.length != 1:
            note = note.with_length_mod(evaluate(context=context, subject=note, how=self.length))

        if self.sharp and evaluate(context=context, subject=note, how=self.sharp):
            note = note.transpose(semitones=1)

        if self.flat and evaluate(context=context, subject=note, how=self.flat):
            note = note.transpose(semitones=-1)

        if self.chord_type:
            note = note.chordify(evaluate(context=context, subject=note, how=self.chord_type))

        if self.track_copy:
            track_name = evaluate(context=context, subject=note, how=self.track_copy)
            track = context.song.find_track_by_name(track_name)
            if track:
                note.with_track_copy(track)


        if self.track_grab:
            note.deferred_expressions.append(
                Deferrable(
                    context  = context,
                    how      = evaluate(context=context, subject=note, how=self.track_grab),
                    function = defer_track_grab
                )
            )

        if self.ccs:
            items = {}
            for (k,v) in self.ccs.items():
                items = {}
                items[k] = evaluate(context=context, subject=note, how=v)
            for (k,v) in items.items():
                note = note.with_cc(k,v)

        if self.delay:
            note = note.with_delay(evaluate(context=context, subject=note, how=self.delay))

        if self.velocity is not None:
            note = note.with_velocity(evaluate(context=context, subject=note, how=self.velocity))

        if self.inversion:
            note = note.invert(evaluate(context=context, subject=note, how=self.inversion))

        return note

# ======================================================================================================================

def defer_track_grab(context=None, track=None, subject=None, how=None):

    other_track = context.song.find_track_by_name(how)

    playing = get_first_playing_note(other_track.name)
    if playing is None:
        return None
    copy_tracks = playing.track_copy
    if copy_tracks and track not in copy_tracks:
        #print("on track (%s), this was not for me" % (track.name))
        return None

    new_note = subject.replace_with_note(playing.name, playing.octave)

    if new_note is None:
        return None

    first = subject
    if first.octave_set_recorded is not None:
        new_note = subject.with_octave(first.octave_set_recorded)

    new_note = subject.transpose(octaves=first.octave_shifts_recorded)

    if playing.from_scale:
        new_note = subject.scale_transpose(playing.from_scale, first.degree_shifts_recorded)

    #print("on track (%s), grabbed (%s)" % (track.name, new_note))
    return new_note


S = Slot