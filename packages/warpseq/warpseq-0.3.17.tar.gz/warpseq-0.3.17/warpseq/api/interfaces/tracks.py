# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.track import Track
from warpseq.api.interfaces.base import CollectionApi

class Tracks(CollectionApi):

    object_class    = Track
    public_fields   = [ 'name', 'instruments', 'instrument_mode', 'muted']
    song_collection = 'tracks'
    add_method      = 'add_tracks'
    add_required    = [ 'muted' ]
    edit_required   = [ ]
    remove_method   = 'remove_track'
    nullable_edits  = [ ]

    def add(self, name, instrument:str=None, instruments:list=None, instrument_mode:str=None, muted:bool=False):
        if not (instrument or (instruments is not None)):
            raise InvalidUsage("either instrument or instruments is required")
        if instruments is None:
            instruments = []
        instruments = [ self.api.instruments.lookup(x, require=True) for x in instruments ]
        if instrument:
            instrument = self.api.instruments.lookup(instrument, require=True)
        return self._generic_add(name, locals())

    def edit(self, name:str=None, id:str=None, new_name:str=None, instrument:str=None, instruments:list=None, instrument_mode:str=None, muted:bool=False):
        if instrument:
            instrument = self.api.instruments.lookup(instrument, require=True)
        if instruments is not None:
            instruments = [self.api.instruments.lookup(x, require=True) for x in instruments]
        return self._generic_edit(name, locals())

    def reorder(self, id=None, direction=None):
        # FIXME: this is a mirror of what is in scenes.py

        object = self.lookup(id=id, require=True)
        assert object is not None
        direction = int(direction)
        count = len(self.song.tracks)
        index = self.song.tracks.index(object)
        if direction == 1:
            if index < count - 1:
                other = self.song.tracks[index+1]
                self.song.tracks[index] = other
                self.song.tracks[index+1] = object
        elif direction == -1:
            if index > 0:
                other = self.song.tracks[index-1]
                self.song.tracks[index] = other
                self.song.tracks[index-1] = object

    def delete(self, id=None, ignore_clips=False):
        obj = self.lookup(id=id, require=True)

        if not ignore_clips:
            clips = self.song.all_clips()
            for c in clips:
                if c.track == obj:
                    # FIXME: most of these methods should also take objects
                    self.api.player.stop_clips([c.name])
                    self.song.remove_clip(scene=c.scene, track=c.track)

        return self._generic_remove(obj.name)