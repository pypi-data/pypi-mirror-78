# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this class is used by the player code to send MIDI events to hardware
# it contains some logic to convert chords to note events and must also
# process deferred mod-expressions caused by late-binding intra-track
# events.

from warpseq.api.callbacks import Callbacks
# from warpseq.api.exceptions import *
from warpseq.model.registers import register_playing_note, unregister_playing_note
from warpseq.model.chord import Chord
from warpseq.model.event import NOTE_OFF, NOTE_ON

# ======================================================================================================================

def _get_note_number(note, instrument):

    max_o = instrument.max_octave
    min_o = instrument.min_octave

    note2 = note.copy().transpose(octaves=instrument.base_octave)

    if note2.octave > max_o:
        note2.octave = max_o
    if note2.octave < min_o:
        note2.octave = min_o

    nn = note2.note_number()

    if nn < 0 or nn > 127:
        print("warning: note outside of playable range: %s" % note2)
        return None

    return nn

# ======================================================================================================================

class RealtimeEngine(object):

    __slots__ = ['midi_out','midi_port','callbacks']

    # ------------------------------------------------------------------------------------------------------------------


    def __init__(self):

        self.callbacks = Callbacks()

    # ------------------------------------------------------------------------------------------------------------------

    def _process_deferred(self, evt):

        exprs = evt.note.deferred_expressions
        for expr in exprs:
            value = expr.evaluate(evt.track, evt.note)
            if value is None:
                evt.note = None
                return
            evt.note = value

    # ------------------------------------------------------------------------------------------------------------------

    def _play_notes(self, event):

        mode = event.track.instrument_mode
        chosen = event.track.before_instrument_select(mode)
        for (i, x) in enumerate(event.note.notes):
            if x.muted:
                return
            evt = event.copy()
            evt.note = x
            evt.instruments = event.track.get_instruments(evt, chosen, mode)
            self._process_deferred(evt)
            if evt.note is None:
                return
            self.play(evt)

    # ------------------------------------------------------------------------------------------------------------------

    def _play_note_on(self, event):



        register_playing_note(event.track, event.note)

        for (control, value) in event.note.ccs.items():
            control = int(control)
            for instrument in event.get_instruments():
                instrument.device.midi_cc(instrument.channel, control, int(value))

        if not (event.track.muted or event.note.muted):

            event.player.inject_off_event(event)

            for instrument in event.get_instruments():

                velocity = event.note.velocity
                if velocity is None:
                    velocity = instrument.default_velocity

                if not instrument.muted:
                    # print("PLAY ON %s: %s" % (self.track.name, event.note))
                    instrument.device.midi_note_on(instrument.channel,
                                 _get_note_number(event.note, instrument), velocity)

    # ------------------------------------------------------------------------------------------------------------------

    def _play_note_off(self, event):

        unregister_playing_note(event.track, event.on_event.note)

        #if event.track.muted:
        #    return

        for instrument in event.get_instruments():

            velocity = event.note.velocity
            if velocity is None:
                velocity = instrument.default_velocity

            if not instrument.muted:
                # print("PLAY OFF ON %s: %s" % (self.track.name, event.note))
                instrument.device.midi_note_off(instrument.channel,
                              _get_note_number(event.note, instrument), velocity)

    # ------------------------------------------------------------------------------------------------------------------

    def play(self, event):

        if not event.note:
            return
        if type(event.note) == Chord:
            self._play_notes(event)
            return
        if event.type == NOTE_ON:
            self._play_note_on(event)
        elif event.type == NOTE_OFF:
            self._play_note_off(event)
        else:
            raise Exception("???")


