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

    def add(self, name, scale:str=None, auto_advance:bool=True, rate:int=1):
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        return self._generic_add(name, params)

    def edit(self, name:str=None, id:str=None, new_name:str=None, scale:str=None, auto_advance:bool=None, rate:int=None):
        if rate:
            try:
                rate = float(rate)
            except:
                rate = 1
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        return self._generic_edit(name, params)

    def reorder(self, id=None, direction=None):
        # FIXME: this is a mirror of what is in tracks.py

        object = self.lookup(id=id, require=True)
        assert object is not None
        direction = int(direction)
        count = len(self.song.scenes)
        index = self.song.scenes.index(object)
        if direction == 1:
            if index < count - 1:
                other = self.song.scenes[index+1]
                self.song.scenes[index] = other
                self.song.scenes[index+1] = object
        elif direction == -1:
            if index > 0:
                other = self.song.scenes[index-1]
                self.song.scenes[index] = other
                self.song.scenes[index-1] = object

    def delete(self, id=None, ignore_clips=False):
        # this object can't be referenced by any other objects so not to much to do here...
        obj = self.lookup(id=id, require=True)

        if not ignore_clips:
            clips = self.song.all_clips()
            for c in clips:
                if c.scene == obj:
                    self.api.player.stop_clips([c.name])
                    self.song.remove_clip(scene=c.scene, track=c.track)

        print("** REMOVING SCENE")
        return self._generic_remove(obj.name)



