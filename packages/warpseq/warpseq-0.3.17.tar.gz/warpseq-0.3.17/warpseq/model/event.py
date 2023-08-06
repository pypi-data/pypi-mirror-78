# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# an event represents starting or stopping a note, and some associated
# data so the program can handle the note and other processing in context.
# for instance the scale is needed for processing deferred events.

import copy

NOTE_ON = 1
NOTE_OFF = 0

class Event(object):


    __slots__ = [ 'type', 'note', 'time', 'on_event', 'from_context', 'instruments', 'song', 'track', 'clip', 'player' ]

    def __init__(self, type=None, note=None, time=None, on_event=None, from_context=None, instruments=None,
                 song=None, track=None, clip=None, player=None):

        self.type = type
        self.note = note
        self.time = time

        self.on_event = on_event
        self.from_context = from_context

        if instruments is None:
            instruments = []

        self.instruments = instruments

        self.song = song
        self.track = track
        self.clip = clip
        self.player = player

    def __repr__(self):
        return "Event<Note=%s, type=%s, time=%s, instruments=%s>" % (self.note, self.type, self.time, self.instruments)

    def get_instruments(self):
        if self.on_event:
            return self.on_event.instruments
        return self.instruments

    def copy(self):
        return Event(
            type = self.type,
            note = self.note.copy(), # could be a Chord!  Be careful.
            time = self.time,
            on_event = self.on_event,
            instruments = self.instruments,
            song = self.song,
            track = self.track,
            clip = self.clip,
            player = self.player
        )
