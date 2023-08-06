# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a clip is a set of patterns and other details at the intersection
# of a scene and track

from ..playback.player import Player
from ..utils import utils
from .base import NewReferenceObject
from .scale import Scale
from warpseq.model.context import Context
from warpseq.model.event import Event, NOTE_ON
from warpseq.model.chord import Chord

# FAIR WARNING: some refactoring still pending

DEFAULT_SCALE = None

def get_default_scale():
    from .note import Note
    global DEFAULT_SCALE
    if DEFAULT_SCALE is None:
        DEFAULT_SCALE = Scale(root=Note(name="C", octave=0), scale_type='chromatic')
    return DEFAULT_SCALE

class Clip(NewReferenceObject):

    __slots__ = [
        'name', 'scales', 'patterns', 'transforms', 'rate', 'repeat', 'auto_scene_advance', 'next_clip', 'tempo_shifts',
        'obj_id', 'slot_length', 'track','scene','_current_tempo_shift','_tempo_roller','_transform_roller',
        '_scale_roller', 'self_destruct_api_reference'
    ]

    SAVE_AS_REFERENCES = [ 'track', 'scene', 'patterns', 'scales', 'transforms' ]


    def __init__(self, name=None, scales=None, patterns=None, transforms=None,  rate=1, repeat=-1,
                 auto_scene_advance=False, next_clip=None, tempo_shifts=None, track=None,
                 scene=None, slot_length=0.0625, obj_id=None, self_destruct_api_reference=None):

        self.name = name
        self.obj_id = obj_id
        self.scales = scales
        self.patterns = patterns

        self.transforms = transforms
        self.rate = rate
        self.repeat = repeat
        self.auto_scene_advance = auto_scene_advance
        self.next_clip = next_clip
        self.tempo_shifts = tempo_shifts
        self.track = track
        self.scene = scene
        self.slot_length = slot_length
        self._current_tempo_shift = 0
        self.self_destruct_api_reference = None

        super(Clip, self).__init__()
        self.reset()

    # ==================================================================================================================

    def reset(self):
        """
        Resetting a clip (restarting it) moves all rolling positions in
        scales and so on to the first position in those lists.
        """

        # FIXME: refactor

        if self.tempo_shifts:
            self._tempo_roller = utils.roller(self.tempo_shifts)
        else:
            self._tempo_roller = utils.roller([0])

        if self.scales:
            self._scale_roller = utils.roller(self.scales)
        else:
            self._scale_roller = None

        if self.transforms is not None:
            self._transform_roller = utils.roller(self.transforms)
        else:
            self._transform_roller = utils.roller([ None ])

    # ==================================================================================================================

    def scenes(self, song):
        return [ song.find_scene(x) for x in self.scene_ids ]

    # ==================================================================================================================

    def tracks(self, song):
        return [ song.find_track(x) for x in self.track_ids ]

    # ==================================================================================================================

    def get_actual_scale(self, song, pattern, roller):
        if roller:
            return next(roller)
        elif pattern and pattern.scale:
            return pattern.scale
        elif self.scene.scale:
            return self.scene.scale
        elif song.scale:
            return song.scale
        return get_default_scale()

    def has_pattern(self, pattern):
        return pattern in self.patterns

    def remove_pattern(self, pattern):
        self.patterns = [ x for x in self.patterns if x != pattern ]

    def has_transform(self, transform):
        for x in self.transforms:
            if x == transform:
                return True
            if type(x) == list and transform in x:
                return True
        return False

    def remove_transform(self, transform):
        results = []
        for x in self.transforms:
            if type(x) == list:
                results.append([a for a in x if a != transform])
            elif x != transform:
                results.append(x)
        self.transforms = results


    # ==================================================================================================================

    def slot_duration(self, song, pattern):
        # in milliseconds
        return (120 / (song.tempo * self.rate * pattern.rate * self.scene.rate + self._current_tempo_shift)) * 125

    # ==================================================================================================================

    def get_clip_duration(self, song):
        # in milliseconds
        total = 0
        for pattern in self.patterns:
            ns = self.slot_duration(song, pattern) * pattern.get_length()
            total = total+ns
        return total

    # ==================================================================================================================

    def _apply_slot_times(self, t_start, slot_duration, chords):
        # given a 2d list of notes apply the start/end time and length info

        start = t_start
        for slot in chords:
            if slot is None:
                pass
            else:
                for note in slot.notes:
                    note.start_time = start
                    note.end_time = note.start_time + slot_duration
                    note.length = slot_duration
            start = start + slot_duration
        return start

    # ==================================================================================================================

    def _process_ties(self, chords):

        previous_chord = None
        tied = 0
        previous_was_tie = False

        for (i, slot) in enumerate(chords):

            if slot and len(slot.notes) and slot.notes[0].tie and previous_chord:
                tied = tied + 1

            if previous_was_tie and previous_chord and ((not slot) or (slot and len(slot.notes) and not slot.notes[0].tie)):
                previous_chord.with_tied(tied * previous_chord.notes[0].length)
                previous_chord = None
                tied = 0

            previous_was_tie = False

            if slot and len(slot.notes):
                if not slot.notes[0].tie:
                    previous_chord = slot
                else:
                    previous_was_tie = True

        if previous_was_tie and previous_chord:
            previous_chord.with_tied(tied * previous_chord.notes[0].length)



    # ==================================================================================================================

    def _notes_to_events(self, chords):

        # given a 1d list of chords, return the list of events with their time info
        # processing tie events along the way and also delay metadata

        events = []
        new_chords = []

        # FIXME: this should be modified to keep the subsystem as chords the whole time
        # through the first part

        # FIXME: smaller functions

        for slot in chords:

            if not slot:
                continue

            if len(slot.notes) and not slot.notes[0].tie:

                tie_bonus = slot.tie_count()

                new_chord = []

                for note in slot.notes:

                    if note is not None and not note.tie and not note.muted:

                        if note.length_mod != 1:
                            note.length = (note.length_mod * note.length)
                            note.end_time = note.start_time + note.length

                        if note.delay:
                            bump = (note.delay * note.length)
                            note.start_time = note.start_time + bump
                            note.end_time = note.end_time + bump

                        if not note.repeat:
                            note.length = note.length + tie_bonus
                            note.end_time = note.end_time + tie_bonus

                        new_chord.append(note)

                new_chords.append(Chord(notes=new_chord))

        for chord in new_chords:

            repeats = chord.notes[0].repeat

            if not repeats:

                event1 = Event(type=NOTE_ON, note=chord,time=int(chord.notes[0].start_time))
                events.append(event1)

            else:

                delta = (chord.notes[0].end_time - chord.notes[0].start_time) / (repeats + 1)

                for x in range(0, repeats):


                    for (j, note) in enumerate(chord.notes):

                        n1 = note.copy()
                        n1.start_time = int(note.start_time + (x*delta))
                        n1.end_time = int(n1.start_time + delta - 1)
                        n1.length = delta - 2

                        if x == note.repeat:
                            n1.length = n1.length + tie_bonus - 1
                        n1.end_time = n1.end_time + tie_bonus - 1

                        event2 = Event(type=NOTE_ON, note=Chord(notes=[n1]), time=int(n1.start_time))

                        events.append(event2)

        return events

    # FIXME: it is no longer true that all inputs will be chords, process deferred exprs with NOTES?

    # ==================================================================================================================

    def _get_pattern_chord_list(self, song, t_start, pattern):

        # ----
        # compute basic info for this pattern

        self._current_tempo_shift = next(self._tempo_roller)
        octave_shift = pattern.get_octave_shift(self.track)
        slot_duration = self.slot_duration(song, pattern)
        scale = self.get_actual_scale(song, pattern, self._scale_roller)

        # -----
        # what transform are we going to apply (if any?)

        if self._transform_roller:
            transform = next(self._transform_roller)
        else:
            transform = None

        context = Context(song = song, clip = self, pattern = pattern, scale = scale, base_length = slot_duration)

        # ----
        # walk each slot in the pattern, then compute length info

        chords = []

        # BOOKMARK: this is the part that will have to nest if we do drum patterns

        for expression in pattern.get_iterator():

            root = scale.get_first().copy()
            root.length = slot_duration
            root.from_context = context

            chord = expression.evaluate(context, root)
            if chord and octave_shift:
                chord = chord.transpose(octaves=octave_shift)
            chords.append(chord)

        self._apply_slot_times(t_start, slot_duration, chords)

        # ---
        # apply any transforms

        if transform:
            if type(transform) != list:
                transform = [transform]
            for tform in transform:
                chords  = tform.process(song, pattern, scale, self.track, chords, t_start, slot_duration)

        # ---
        # we return a list of chords per slot

        return chords

    # ==================================================================================================================

    def get_events(self, song):
        """
        Return all the event objects for the clip.
        """

        t_start = 0
        chords_out = []

        for pattern in self.patterns:

            # get all the chords for each step
            chords = self._get_pattern_chord_list(song, t_start, pattern)
            chords_out.extend(chords)
            t_start = t_start + (self.slot_duration(song, pattern) * pattern.get_length())

        # convert to events
        self._process_ties(chords_out)
        return self._notes_to_events(chords_out)



    # ==================================================================================================================

    def get_player(self, song, engine_class):
        player = Player(
            clip=self,
            song=song,
            engine=engine_class(),
        )
        return player
