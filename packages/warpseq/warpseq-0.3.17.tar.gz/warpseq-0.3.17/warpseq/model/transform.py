# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a transform is a list of modifier expressions that can be used
# to build MIDI effects including Arps.

from ..utils.utils import roller
from .base import NewReferenceObject
from .directions import *
from warpseq.model.context import Context
from warpseq.model.slot import Slot
import sys

CHORDS = 'chords'
NOTES = 'notes'
BOTH = 'both'
APPLIES_CHOICES = [ CHORDS, NOTES, BOTH ]

class Transform(NewReferenceObject, Directionable):

    __slots__ = [ 'name', 'slots', 'arp', '_current_slots', 'divide', 'applies_to', 'obj_id',
                  'direction', '_current_direction', '_iterator', '_slot_mods', 'auto_reset', 'audition_instrument',
                  'audition_pattern']

    SAVE_AS_REFERENCES = [ 'audition_instrument', 'audition_pattern' ]

    # ==================================================================================================================

    def __init__(self, name=None, slots=None, divide=None, obj_id=None,
                 applies_to=BOTH, direction=FORWARD, auto_reset=False, arp=True, audition_instrument=None,
                 audition_pattern=None):

        # FIXME: TEMPORARY! we'll add in web_slots compile soon ... this is just for UI testing!
        if slots is None:
            slots = [
                Slot(octave_shift=1),
                Slot(degree=2),
                Slot(octave_shift=-1),
                Slot(),
                Slot(repeats=4),
                Slot(length=0.5),
                Slot(rest=True),
                Slot(repeats=2)
            ]

        # we'll add in web_slots compile soon
        if slots is None:
            slots = []

        self.name = name
        self.slots = slots



        for x in slots:
            assert isinstance(x, Slot)

        self.divide = divide
        self.applies_to = applies_to
        self.obj_id = obj_id
        self._slot_mods = roller(slots)
        self.direction = direction
        self._current_direction = direction
        self.auto_reset = auto_reset
        self.applies_to = applies_to
        self.audition_instrument = audition_instrument
        self.audition_pattern = audition_pattern
        self.arp = arp

        assert applies_to in APPLIES_CHOICES
        self.reset()

        super(Transform, self).__init__()

    # ==================================================================================================================

    def _get_should_process_and_arpeggiate(self, chord):
        # what should happen to this chord/note ?

        process = True
        arpeggiate = True

        if len(chord.notes) == 1:
            if self.applies_to not in [BOTH, NOTES]:
                process = False
                arpeggiate = False
        else:
            if self.applies_to not in [BOTH, CHORDS]:
                process = False
                arpeggiate = False

        return (process, arpeggiate)

    # ==================================================================================================================

    def _get_effective_divide(self, chord):
        # how many steps should we slice this into?

        if self.divide is not None:
            return self.divide
        return len(chord.notes)

    # ==================================================================================================================

    def _get_notes_iterator(self, chord, arpeggiate):
        # what should we play as we repeat this step?

        if not arpeggiate:
            return utils.forever(chord)
        return utils.roller(chord.notes)

    # ==================================================================================================================

    def process(self, song, pattern, scale, track, chord_list, t_start, slot_duration):

        results = []
        context = Context(song=song, pattern=pattern, scale=scale, track=track, base_length=slot_duration)

        if self.auto_reset:
            self.reset()

        for chord in chord_list:

            if chord is None:
                continue

            (process, arpeggiate) = self._get_should_process_and_arpeggiate(chord)
            divide = self._get_effective_divide(chord)

            if not self.arp:
                arpeggiate = False

            notes_iterator = self._get_notes_iterator(chord, arpeggiate)

            original_start = chord.notes[0].start_time
            original_end = chord.notes[0].end_time
            delta = original_end - original_start
            new_delta = delta / divide

            n_start = original_start
            n_end = original_start + new_delta

            for _ in range(0, divide):

                my_slot = self.get_next()

                this_note = next(notes_iterator)
                transformed = my_slot.evaluate(context, this_note)

                if transformed is None:
                    results.append([])
                    continue

                results.append(transformed.with_timing(
                    start_time = n_start,
                    end_time = n_end,
                    length = new_delta
                ))

                n_start = n_start + new_delta
                n_end = n_end + new_delta

        return results

