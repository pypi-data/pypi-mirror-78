# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.data_pool import DataPool
from warpseq.api.interfaces.base import CollectionApi

class DataPools(CollectionApi):

    object_class    = DataPool
    public_fields   = [ 'name', 'slots', 'direction', 'length' ]
    song_collection = 'data_pools'
    add_method      = 'add_data_pools'
    add_required    = [ 'slots' ]
    edit_required   = [ ]
    remove_method   = 'remove_data_pool'

    def add(self, name, slots:list=None, direction='forward', length=None):
        params = locals()
        return self._generic_add(name, params)

    def edit(self, name:str=None, id:str=None, new_name:str=None, slots:list=None, direction=None, length=None):
        params = locals()
        return self._generic_edit(name, params)

    def delete(self, id=None):
        obj = self.lookup(id=id, require=True)
        return self._generic_remove(obj.name)