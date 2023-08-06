# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.clip import Clip
from warpseq.api.interfaces.base import CollectionApi

class Clips(CollectionApi):

    object_class    = Clip
    public_fields   = [ 'name', 'scene', 'track', 'patterns',
                        'tempo_shifts', 'next_clip', 'transforms',
                        'repeat' ]
    song_collection = 'clips'
    add_method      = 'add_clip'
    add_required    = [ 'scene', 'track', 'patterns' ]
    edit_required   = [ 'scene', 'track' ]
    remove_method   = 'remove_clip'
    nullable_edits  = [ 'tempo', 'repeat' ]

    # this is relatively dark because the clips are anything but generic, living at the intersection of a 2D
    # grid and the names are not unique

    def _lookup_transforms(self, alist):
        results = []
        for x in alist:
            if type(x) == list:
                results.append([ self.api.transforms.lookup(i, require=True) for i in x])
            else:
                results.append(self.api.transforms.lookup(x))
        return results

    def add(self, name, scene:str=None, track:str=None, patterns:list=None,
            tempo_shifts:list=None, next_clip:str=None,
            transforms:list=None, repeat:int=None, auto_scene_advance:bool=False, scales:list=None, rate:int=1):

        if patterns:
            patterns = [ self.api.patterns.lookup(p, require=True) for p in patterns ]
        if transforms:
            transforms = self._lookup_transforms(transforms)
        if scales:
            scales = [ self.api.scales.lookup(s, require=True) for s in scales ]
        params = locals()

        clip = Clip(name=name, patterns=patterns, tempo_shifts=tempo_shifts, next_clip=next_clip,
                 transforms=transforms, auto_scene_advance=auto_scene_advance, repeat=repeat, scales=scales, rate=rate)

        scene = self.api.scenes.lookup(scene, require=True)
        track = self.api.tracks.lookup(track, require=True)

        self.song.add_clip(scene=scene, track=track, clip=clip)
        return self._ok()


    def edit(self, name:str=None, id:str=None, new_name:str=None, scene: str = None, track:str = None, patterns: list = None,
            tempo_shifts: list = None, next_clip:str = None,
            transforms:list = None, repeat:int=None, auto_scene_advance:bool=False, scales:list=None, rate:int=None):

        scene = self.api.scenes.lookup(scene, require=True)
        track = self.api.tracks.lookup(track, require=True)

        params = locals()

        if patterns:
            params["patterns"] = [ self.api.patterns.lookup(p, require=True) for p in patterns ]
        if transforms:
            params["transforms"] = self._lookup_transforms(transforms)
        if scales:
            params["scales"] = [ self.api.scales.lookup(s, require=True) for s in scales ]

        if new_name is not None:
            params["name"] = params["new_name"]
        else:
            del params["name"]
        del params["new_name"]

        if params["next_clip"]:
            # validate but keep it a string
            self.api.clips.lookup(params["next_clip"], require=True)


        obj = self.song.get_clip_for_scene_and_track(scene, track)
        if obj is None:
            raise InvalidInput("clip not found for scene (%s) and track (%s)" % (scene.name, track.name))

        for (k,v) in params.items():
            if k == 'self':
                continue
            if k in self.__class__.nullable_edits or v is not None:
                setattr(obj, k, v)

        return self._ok()

    def remove(self, scene:str=None, track:str=None):

        scene = self.api.scenes.lookup(scene, require=True)
        track = self.api.tracks.lookup(track, require=True)
        self.song.remove_clip(scene,track)
        return self._ok()

    def _short_details(self, obj):
        return dict(name=obj.name, scene=obj.scene.name, track=obj.track.name, obj_id=obj.obj_id)

    def delete(self, id=None):
        obj = self.lookup(id=id, require=True)
        self.api.player.multi_player.remove_clip(obj)
        return self._generic_remove(obj.name)
