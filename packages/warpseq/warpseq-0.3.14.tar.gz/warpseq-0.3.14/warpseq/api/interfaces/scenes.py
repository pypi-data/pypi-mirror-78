# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.scene import Scene
from warpseq.api.interfaces.base import CollectionApi

class Scenes(CollectionApi):

    object_class    = Scene
    public_fields   = [ 'name', 'scale', 'auto_advance', 'rate' ]
    song_collection = 'scenes'
    add_method      = 'add_scenes'
    add_required    = [ ]
    edit_required   = [ ]
    remove_method   = 'remove_scene'
    nullable_edits  = [ 'tempo', 'scale' ]

    def add(self, name, scale:str=None, auto_advance:bool=None, rate:int=1):
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        return self._generic_add(name, params)

    def edit(self, name, id:str=None, new_name:str=None, scale:str=None, auto_advance:bool=None, rate:int=None):
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        return self._generic_edit(name, params)