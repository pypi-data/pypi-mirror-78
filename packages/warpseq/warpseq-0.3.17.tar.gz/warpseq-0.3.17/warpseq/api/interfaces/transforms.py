# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.transform import Transform
from warpseq.api.interfaces.base import CollectionApi

class Transforms(CollectionApi):

    object_class     = Transform
    public_fields    = [ 'name', 'divide', 'applies_to', 'direction', 'auto_reset', 'arp', 'audition_instrument', 'audition_pattern' ]
    song_collection  = 'transforms'
    add_method       = 'add_transforms'
    add_required     = [ 'slots' ]
    edit_required    = [ ]
    remove_method    = 'remove_transform'
    nullable_edits   = [ ]

    def add(self, name, slots:list=None, divide:int=None, applies_to:str='both', direction='forward', arp=True, auto_reset=False):
        params = locals()
        return self._generic_add(name, params)

    def edit(self, name:str=None, id:str=None, new_name:str=None, slots:list=None, divide:int=None, applies_to:str=None, arp:bool=None,
             direction=None, auto_reset=None, audition_instrument=None, audition_pattern=None):

        if audition_instrument:
            audition_instrument = self.api.instruments.lookup(audition_instrument, require=True)
        if audition_instrument:
            audition_pattern = self.api.patterns.lookup(audition_pattern, require=True)

        if divide == "auto":
            divide = None
        if divide is not None:
            try:
                divide = int(divide)
            except:
                divide = 1
        params = locals()
        return self._generic_edit(name, params)

    def delete(self, id=None):

        obj = self.lookup(id=id, require=True)
        assert obj is not None

        # patterns can be used in any clip, so we have to trim them
        # if we find them playing in any clips we must also stop those

        for clip in self.song.all_clips():

            if clip.has_transform(obj):
                self.api.player.stop_clips([clip.name])
                clip.remove_transform(obj)

        return self._generic_remove(obj.name)


    # ------------------------------------------------------------------------------------------------------------------

    def audition(self, name:str=None, id:str=None):

        obj = self.lookup(name=name, id=id, require=True)

        if (not obj.audition_pattern) or (not obj.audition_instrument):
            print ("FAILED!")
            return False

        pattern_id = obj.audition_pattern.obj_id


        self.api.patterns.audition(
            id=pattern_id,
            override_instrument=obj.audition_instrument,
            transforms=[obj]
        )

        return None
