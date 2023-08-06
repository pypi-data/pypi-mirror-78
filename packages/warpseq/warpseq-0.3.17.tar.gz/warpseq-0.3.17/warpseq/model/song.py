# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# the song is the fundamental unit of saving/loading in Warp and contains
# all object types.

import json

from warpseq.model.base import NewReferenceObject

FORMAT_VERSION = 0.1
DEFAULT_NAME = 'Warp Song'

class Song(NewReferenceObject):

    # FIXME: warning slot order might matter as it is used by the serializer

    __slots__ = [ 'name',  'devices', 'instruments', 'tracks', 'clips', 'scale', 'tempo',  'scales', 'scenes',
                  'transforms', 'patterns', 'data_pools', 'obj_id', 'filename' ]

    SAVE_AS_REFERENCES = []

    def __init__(self, name='Warp Song', clips = None, scale=None, tempo=120, devices=None, instruments=None, scales=None,
                 scenes=None, tracks=None, transforms=None, patterns=None, data_pools=None, obj_id=None, filename='warp.json'):

        self.name = name
        self.clips = clips
        self.scale = scale
        self.tempo = tempo
        self.devices = devices
        self.instruments = instruments
        self.scales = scales
        self.scenes = scenes
        self.tracks = tracks
        self.transforms = transforms
        self.patterns = patterns
        self.data_pools = data_pools
        self.obj_id = obj_id
        self.filename = filename

        super(Song, self).__init__()

        self.reset(clear=False)

    def details(self):
        # return public fields - this is a bit different from other classes as this is the top level object
        results =  dict(
            name = self.name,
            tempo = self.tempo,
            filename = self.filename,
        )
        if self.scale:
            results['scale'] = self.scale.name
        else:
            results['scale'] = None
        return results

    def reset(self, clear=True):
        if clear or self.devices is None:
            self.devices = dict()
        if clear or self.instruments is None:
            self.instruments = dict()
        if clear or self.scales is None:
            self.scales = dict()
        if clear or self.tracks is None:
            self.tracks = []
        if clear or self.scenes is None:
            self.scenes = []
        if clear or self.clips is None:
            self.clips = dict()
        if clear or self.transforms is None:
            self.transforms = dict()
        if clear or self.patterns is None:
            self.patterns = dict()
        if clear or self.data_pools is None:
            self.data_pools = dict()
        if clear:
            self.filename = ""

    def find_device(self, obj_id):
        """
        Returns the device with the given object ID.
        This method and others like this are used for save/load support.
        """
        return self.devices.get(obj_id, None)

    def find_instrument(self, obj_id):
        """
        Returns the instrument with the given object ID.
        """
        return self.instruments.get(str(obj_id), None)

    def find_scale(self, obj_id):
        """
        Returns the scale with the given object ID.
        """
        return self.scales.get(str(obj_id), None)

    def find_scene(self, obj_id):
        """
        Returns the scene with the given object ID.
        """
        print("SCENES: %s" % self.scenes)
        matching = [ x for x in self.scenes if str(x.obj_id) == str(obj_id) ]
        if len(matching) == 0:
            return None
        return matching[0]

    def find_track(self, obj_id):
        """
        Returns the track with the given object ID.
        """
        matching = [ x for x in self.tracks if str(x.obj_id) == str(obj_id) ]
        if len(matching) == 0:
            return None

        #print("FOUND A TRACK")
        #print("*********")
        #print("INST=%s" % matching[0].instruments)
        #raise Exception("STOP!")

        return matching[0]

    def find_clip(self, obj_id):
        """
        Returns the clip with the given object ID.
        """
        return self.clips.get(str(obj_id), None)

    def find_clip_by_name(self, name):
        """
        Returns the clip with the given name.
        """
        for (k,v) in self.clips.items():
            if v.name == name:
                return v
        return None

    def find_track_by_name(self, name):
        for v in self.tracks:
            if v.name == name:
                return v
        return None

    def find_transform(self, obj_id):
        """
        Returns the transform with the given object ID.
        """
        x = self.transforms.get(str(obj_id), None)
        return x

    def find_pattern(self, obj_id):
        """
        Returns the pattern with the given object ID.
        """
        return self.patterns.get(str(obj_id), None)

    def find_data_pool(self, obj_id):
        return self.data_pools.get(str(obj_id), None)

    def find_pattern_by_name(self, name):
        for (k,v) in self.patterns.items():
            if v.name == name:
                return v
        return None

    def find_data_pool_by_name(self, name):
        for (k,v) in self.data_pools.items():
            if v.name == name:
                return v
        return None

    def to_dict(self):
        """
        Returns the data for the entire song file.
        This can be reversed with from_dict.
        """
        global FORMAT_VERSION
        data = super().to_dict()
        data['FORMAT_VERSION'] = FORMAT_VERSION
        data['OBJ_COUNTER'] = NewReferenceObject.new_object_id()
        #print("SONG=%s" % json.dumps(data, sort_keys=True, indent=4))
        return data

    def to_json(self):
        """
        Returns a saveable JSON version of the song file.
        """
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    @classmethod
    def from_dict(cls, data):


        # FIXME: TODO: we should be able to use the deserializer here too?

        """
        Loads a song from a dictionary.
        This must support PAST but not FUTURE versions of the program.
        """

        song = Song(name=data['name'])

        from . base import COUNTER

        format_version = data.get('FORMAT_VERSION', 0)
        if format_version > FORMAT_VERSION:
            # FIXME:  change exception type
            print("can not open data from a newer version of this program")

        COUNTER = data['OBJ_COUNTER']

        song.obj_id = data['obj_id']

        from . device import Device
        from . instrument import Instrument
        from . scale import Scale
        from . scene import Scene
        from . track import Track
        from . clip import Clip
        from . transform import Transform
        from . pattern import Pattern
        from . data_pool import DataPool

        song.scales = { str(k) : Scale.from_dict(song, v) for (k,v) in data['scales'].items() }
        song.devices = { str(k) : Device.from_dict(song, v) for (k,v) in data['devices'].items() }
        song.instruments =  { str(k) : Instrument.from_dict(song, v) for (k,v) in data['instruments'].items() }

        song.scenes = [ Scene.from_dict(song, v) for v in data['scenes'] ]
        song.tracks = [ Track.from_dict(song, v) for v in data['tracks'] ]

        song.transforms =  {str(k) : Transform.from_dict(song, v) for (k, v) in data['transforms'].items()}
        song.patterns =  { str(k) : Pattern.from_dict(song, v) for (k,v) in data['patterns'].items() }
        song.data_pools =  { str(k) : DataPool.from_dict(song, v) for (k,v) in data['data_pools'].items() }

        song.clips =  { str(k) : Clip.from_dict(song, v) for (k,v) in data['clips'].items() }

        song.scale = song.find_scale(data['scale'])
        song.tempo = data['tempo']

        return song

    def all_clips(self):
        return [ x for x in self.clips.values() ]

    def all_patterns(self):
        return [ x for x in self.patterns.values() ]

    def next_scene(self, scene):
        """
        Returns the scene that is positioned after this one in the song.
        This uses the scene array, implying (FIMXE) we need a method to reorder scenes.
        """
        index = None
        for (i,x) in enumerate(self.scenes):
            if x.obj_id == scene.obj_id:
                index = i
                break
        index = index + 1
        if index >= len(self.scenes):
            return None
        return self.scenes[index]

    @classmethod
    def from_json(cls, data):
        """
        Loads the song from JSON data, such as from a save file.
        """
        data = json.loads(data)
        return Song.from_dict(data)

    def _get_clip_index(self, scene=None, track=None):
        """
        Internal storage of clip uses a dict where the key is the combination of
        the scene and track object IDs.
        """
        index = "%s/%s" % (scene.obj_id, track.obj_id)
        return index

    def add_clip(self, scene=None, track=None, clip=None):
        """
        Adds a clip at the intersection of a scene and track.
        """

        # calling code must *COPY* the clip before assigning, because a clip must be added
        # to the clip list and *ALSO* knows its scene and track.

        previous = self.get_clip_for_scene_and_track(scene=scene, track=track)
        if previous and clip.obj_id == previous.obj_id:
            return

        if previous:
            self.remove_clip(scene=scene, track=track)

        self.clips[str(clip.obj_id)] = clip

        clip.track = track
        clip.scene = scene

        #assert clip.scene is not None

        track.add_clip(clip)
        scene.add_clip(clip)

        #assert clip.track is not None
        #assert clip.scene is not None

        return clip

    def remove_clip(self, scene=None, track=None):
        """
        Deletes a clip.  The name isn't used - specify the scene and track.
        """

        # removing a clip returns a clip object that can be used with *assign* to add the
        # clip back.

        #assert scene is not None
        #assert track is not None

        clip = self.get_clip_for_scene_and_track(scene=scene, track=track)
        if clip is None:
            return None

        track.remove_clip(clip)
        scene.remove_clip(clip)

        clip.track = None
        clip.scene = None

        del self.clips[clip.obj_id]

        return clip

    def get_clips_for_scene(self, scene=None):
        """
        Returns all clips in a given scene.
        """
        return scene.clips()

    def get_clip_for_scene_and_track(self, scene=None, track=None):
        """
        Returns the clip at the intersection of the scene and track.
        """
        #assert scene is not None
        #assert track is not None
        results = []
        clips = scene.clips(self)
        for clip in clips:
            if track.has_clip(clip):
                results.append(clip)
        return self.one(results)

    def add_devices(self, devices):
        """
        Adds some device objects to the song.
        """
        for x in devices:
            self.devices[str(x.obj_id)] = x

    def remove_device(self, device):
        """
        Removes a device from the song.
        """
        del self.devices[str(device.obj_id)]

    def add_instruments(self, instruments):
        """
        Adds some instrument objects to the song
        """
        for x in instruments:
            self.instruments[str(x.obj_id)] = x

    def remove_instrument(self, instrument):
        """
        Removes an instrument object from the song.
        """
        del self.instruments[str(instrument.obj_id)]

    def add_scales(self, scales):
        """
        Adds some scale objects to a song.
        """
        for x in scales:
            self.scales[str(x.obj_id)] = x

    def remove_scale(self, scale):
        """
        Removes a scale object from the song.
        """
        del self.scales[str(scale.obj_id)]

    def add_tracks(self, tracks):
        """
        Adds some track objects to the song.
        """
        self.tracks.extend(tracks)

    def remove_track(self, track):
        """
        Remove a track object from the song.
        """
        self.tracks = [ t for t in self.tracks if t.obj_id != track.obj_id ]

    def add_scenes(self, scenes):
        """
        Adds some scene objects to the song.
        """
        self.scenes.extend(scenes)

    def remove_scene(self, scene):
        """
        Removes a scene object from the song.
        """
        self.scenes = [ s for s in self.scenes if s.obj_id != scene.obj_id ]

    def add_patterns(self, patterns):
        """
        Adds some pattern objects to the song.
        """
        for x in patterns:
            self.patterns[str(x.obj_id)] = x

    def remove_pattern(self, pattern):
        """
        Removes a pattern object from the song.
        """
        del self.patterns[str(pattern.obj_id)]

    def add_data_pools(self, data_pools):
        """
        Adds some pattern objects to the song.
        """
        for x in data_pools:
            self.data_pools[str(x.obj_id)] = x

    def remove_data_pool(self, data_pool):
        """
        Removes a pattern object from the song.
        """
        del self.data_pools[str(data_pool.obj_id)]

    def add_transforms(self, transforms):
        """
        Adds some transform objects to the song.
        """
        #assert type(transforms) == list
        for x in transforms:
            self.transforms[str(x.obj_id)] = x

    def remove_transform(self, transform):
        """
        Removes a transform object from the song.
        """
        del self.transforms[str(transform.obj_id)]
