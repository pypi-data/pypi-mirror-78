# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a device represents a physical or virtual MIDI interface

from .base import NewReferenceObject
from warpseq.playback.midi import open_port
from warpseq.playback.midi import midi_note_on, midi_note_off, midi_cc

class Device(NewReferenceObject):

    __slots__ = [ 'name', 'obj_id', '_midi_out', ]

    SAVE_AS_REFERENCES = []

    def __init__(self, name=None, obj_id=None):
        self.name = name
        self.obj_id = obj_id
        self._midi_out = None
        super(Device,self).__init__()

    def get_midi_out(self):
        if self._midi_out is None:
            self._midi_out = open_port(self.name)
        return self._midi_out

    def midi_note_on(self, channel, note_number, velocity):
        midi_note_on(self.get_midi_out(), channel, note_number, velocity)

    def midi_note_off(self, channel, note_number, velocity):
        midi_note_off(self.get_midi_out(), channel, note_number, velocity)

    def midi_cc(self, channel, controller, value):
        midi_cc(self.get_midi_out(), channel, controller, value)
