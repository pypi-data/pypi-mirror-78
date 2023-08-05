# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.pattern import Pattern
from warpseq.api.interfaces.base import CollectionApi

class Patterns(CollectionApi):

    object_class    = Pattern
    public_fields   = [ 'name', 'slots', 'octave_shift', 'scale', 'rate', 'direction', 'length']
    song_collection = 'patterns'
    add_method      = 'add_patterns'
    add_required    = [ 'slots' ]
    edit_required   = [ ]
    remove_method   = 'remove_pattern'
    nullable_edits   = [ 'scale ']

    def add(self, name, slots:list=None, scale=None, octave_shift=None, rate=1, direction='forward', length=None):
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        return self._generic_add(name, params)

    def edit(self, name, id:str=None, new_name:str=None, slots:list=None, scale=None, octave_shift=None, rate=None,  direction=None, length=None):
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        return self._generic_edit(name, params)

    def delete(self, id=None):
        raise Exception("NOT IMPLEMENTED YET")