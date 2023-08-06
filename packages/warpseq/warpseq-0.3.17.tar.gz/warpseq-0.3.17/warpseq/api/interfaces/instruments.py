# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.instrument import Instrument
from warpseq.api.interfaces.base import CollectionApi

class Instruments(CollectionApi):

    object_class    = Instrument
    public_fields   = [ 'name', 'channel', 'device', 'muted', 'min_octave', 'max_octave', 'base_octave', 'default_velocity' ]
    song_collection = 'instruments'
    add_method      = 'add_instruments'
    add_required    = [ 'channel', 'device']
    edit_required   = [ ]
    remove_method   = 'remove_instrument'
    nullable_edits  = [ ]

    def add(self, name, channel:int=1, device:str=None, min_octave:int=0, max_octave:int=10, base_octave:int=3, muted:bool=False, default_velocity:int=120):
        device = self.api.devices.lookup(device, require=True)
        return self._generic_add(name, locals())

    def edit(self, name=None, id:str=None, new_name:str=None, channel:int=None, device:str=None, min_octave:int=None, max_octave:int=None, base_octave:int=None, muted:bool=None, default_velocity:int=0):

        # because type hints are not useful, apparently
        if min_octave is not None:
            min_octave = int(min_octave)
        if max_octave is not None:
            max_octave = int(max_octave)
        if base_octave is not None:
            base_octave = int(base_octave)
        else:
            base_octave = 0
        if channel is not None:
            channel = int(channel)

        device = self.api.devices.lookup(device, require=True)
        return self._generic_edit(name, locals())

    def delete(self, id=None):
        obj = self.lookup(id=id, require=True)

        for track in self.song.tracks:
            if track.instruments:
                track.instruments = [ x for x in track.instruments if x != obj ]

        return self._generic_remove(obj.name)

