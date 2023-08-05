# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.transform import Transform
from warpseq.api.interfaces.base import CollectionApi

class Transforms(CollectionApi):

    object_class     = Transform
    public_fields    = [ 'name', 'slots', 'divide', 'applies_to', 'direction', 'auto_reset' ]
    song_collection  = 'transforms'
    add_method       = 'add_transforms'
    add_required     = [ 'slots' ]
    edit_required    = [ ]
    remove_method    = 'remove_transform'
    nullable_edits   = [ ]

    def add(self, name, slots:list=None, divide:int=None, applies_to:str='both', direction='forward', auto_reset=False):
        params = locals()
        return self._generic_add(name, params)

    def edit(self, name, id:str=None, new_name:str=None, slots:list=None, divide:int=1, applies_to:str=None, direction=None, auto_reset=None):
        params = locals()
        return self._generic_edit(name, params)

    def delete(self, id=None):
        raise Exception("NOT IMPLEMENTED YET")