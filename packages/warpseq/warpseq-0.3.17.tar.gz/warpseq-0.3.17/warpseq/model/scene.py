# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a scene is a set of clips that usually play together at the same time.

from .base import NewReferenceObject

class Scene(NewReferenceObject):

    __slots__ = ('name', 'scale', 'auto_advance', 'rate', 'clip_ids', 'obj_id', 'hidden' )

    SAVE_AS_REFERENCES = [ 'scale', ]

    def __init__(self, name=None, scale=None, auto_advance=True, rate=1, clip_ids=None, obj_id=None, hidden=False):

        self.name = name
        self.scale = scale
        self.auto_advance = auto_advance
        self.rate = rate
        self.clip_ids = clip_ids
        self.obj_id = obj_id
        self.hidden = hidden

        if self.clip_ids is None:
            self.clip_ids = []

        super(Scene, self).__init__()

    def clips(self, song):
        results = [ song.find_clip(x) for x in self.clip_ids ]
        results = [ r for r in results if r is not None ]
        return results

    def add_clip(self, clip):
        if clip.obj_id not in self.clip_ids:
            self.clip_ids.append(clip.obj_id)

    def has_clip(self, clip):
        return clip.obj_id in self.clip_ids

    def remove_clip(self, clip):
        self.clip_ids = [ c for c in self.clip_ids if c != clip.obj_id ]

    def is_hidden(self):
        return self.hidden