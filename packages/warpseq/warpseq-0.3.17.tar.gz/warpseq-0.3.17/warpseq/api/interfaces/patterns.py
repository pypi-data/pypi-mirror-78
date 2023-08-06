# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.pattern import Pattern
from warpseq.api.interfaces.base import CollectionApi
from warpseq.api.exceptions import NotFound

INTERNAL_AUDITION_SCENE = "!!INTERNAL/AUDITION_SCENE"
INTERNAL_AUDITION_TRACK = "!!INTERNAL/AUDITION_TRACK"
INTERNAL_AUDITION_CLIP  = "!!INTERNAL/AUDITION_CLIP"

class Patterns(CollectionApi):

    object_class    = Pattern
    public_fields   = [ 'name', 'octave_shift', 'scale', 'rate', 'direction', 'length', 'audition_with', 'is_drum']
    song_collection = 'patterns'
    add_method      = 'add_patterns'
    add_required    = [ 'slots' ]
    edit_required   = [ ]
    remove_method   = 'remove_pattern'
    nullable_edits   = [ 'scale' ]

    # ------------------------------------------------------------------------------------------------------------------

    def add(self, name, slots:list=None, scale=None, octave_shift=None, rate=1, direction='forward',
            audition_with=None, length=None):

        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        if audition_with:
            audition_with = self.api.instruments.lookup(audition_with, require=True)
        params = locals()
        return self._generic_add(name, params)

    # ------------------------------------------------------------------------------------------------------------------

    def edit(self, name:str=None, id:str=None, new_name:str=None, slots:list=None, scale:str=None, octave_shift:int=None,
             rate:int=None,  direction:str=None, length:int=None, audition_with:str=None, web_slots:dict=None, pattern_type:str=None):

        # FIXME: helper methods for casting
        # FIXME: deal with realization that UI uses edit and only user API uses ad, making coverage suboptimal
        # from tests. Can these be combined if we rewrite the CollectionApi code?

        if scale:
            scale = self.api.scales.lookup(scale, require=True)

        if audition_with:
            audition_with = self.api.instruments.lookup(audition_with, require=True)

        if rate is not None:
            try:
                rate = float(rate)
            except:
                rate = 1

        if octave_shift is not None:
            try:
                octave_shift = int(octave_shfit)
            except:
                octave_shift = 0
        else:
            octave_shift = 0

        if length:
            try:
                length = int(length)
            except:
                length = None
        else:
            length = None

        params = locals()
        return self._generic_edit(name, params)

    # ------------------------------------------------------------------------------------------------------------------

    def delete(self, id=None):

        obj = self.lookup(id=id, require=True)
        assert obj is not None

        # patterns can be used in any clip, so we have to trim them
        # if we find them playing in any clips we must also stop those

        for clip in self.song.all_clips():


            if clip.has_pattern(obj):
                self.api.player.stop_clips([clip.name])
                clip.remove_pattern(obj)

        return self._generic_remove(obj.name)

    # ------------------------------------------------------------------------------------------------------------------

    def get_web_slot_grid_for_ui(self, id:str=None, category:str=None):

        obj = self.lookup(id=id, require=True)
        return obj.get_web_slot_grid_for_ui(category)

    def update_web_slots_for_ui(self, id:str=None, data=None):
        obj = self.lookup(id=id, require=True)
        return obj.update_web_slots_for_ui(data)

    # ------------------------------------------------------------------------------------------------------------------

    def audition(self, name:str=None, id:str=None, override_instrument=None, transforms=None):
        """
        This is a *UI ONLY* command to listen to a pattern without having it placed in a clip/song.
        """

        # FIXME: Transform API code reuses this method by passing in override_instrument and transforms though
        # these last two parameters should not be used directly. This should be refactored to mostly
        # call into another shared class that takes object parameters, not IDs.

        from warpseq.model.scene import Scene
        from warpseq.model.track import Track
        from warpseq.model.clip import Clip

        # we can pass in a list of transforms, as intended for use in transforms.audition
        if transforms is None:
            transforms = []

        # find this pattern by name or ID
        obj = self.lookup(id=id, name=name, require=True)

        # we require an instrument to audition the clip
        if obj.audition_with:
            inst = obj.audition_with
        else:
            inst = override_instrument
        if inst is None:
            print("NO INST")
            return False

        # construct a temp scene/track/and clip that will be deleted when we are done
        temp_scene = self.api.scenes.lookup(name=INTERNAL_AUDITION_SCENE)
        if not temp_scene:
            temp_scene = Scene(name=INTERNAL_AUDITION_SCENE, obj_id=INTERNAL_AUDITION_SCENE, auto_advance=False, hidden=True)
            self.song.add_scenes([temp_scene])

        temp_track = self.api.tracks.lookup(name=INTERNAL_AUDITION_TRACK)

        if not temp_track:
            temp_track = Track(name=INTERNAL_AUDITION_TRACK, obj_id=INTERNAL_AUDITION_TRACK,
                               instruments=[inst], hidden=True)
            self.song.add_tracks([temp_track])

        temp_clip = self.song.get_clip_for_scene_and_track(scene=temp_scene, track=temp_track)
        if not temp_clip:
            temp_clip = Clip(name=INTERNAL_AUDITION_CLIP, obj_id=INTERNAL_AUDITION_CLIP, patterns=[obj],
                             transforms=transforms, repeat=None, auto_scene_advance=False)
            self.song.add_clip(scene=temp_scene, track=temp_track, clip=temp_clip)
        else:
            temp_clip.patterns = [obj]
            temp_clip.transforms = transforms

        # run a new event loop with the infinitely repeating clip
        self.api.player.loop(temp_scene.name, stop_if_empty=True)

        # we'll exit this loop when a stop command comes in
        try:
            self.api.scenes.delete(id=temp_scene.obj_id, ignore_clips=True)
            self.api.tracks.delete(id=temp_track.obj_id, ignore_clips=True)
        except NotFound:
            pass

        return None


