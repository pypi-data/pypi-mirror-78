# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# the api router decides what API calls to make for incoming
# service packet requests

from warpseq.server.packet import ResponsePacket
from warpseq.api.exceptions import InvalidOpcode, StopException
import traceback
from warpseq.model.note import NOTES, SCALE_DEGREES_FOR_UI
from warpseq.model.scale import SCALE_TYPES

# ======================================================================================================================
# COMMAND OPCODES

# FIXME: this is dumb, just use getattr. Sometime.

HELLO = 'hello'

FILE_NEW = 'file_new'
FILE_LOAD = 'file_load'
FILE_SAVE = 'file_save'
DATA_LOAD = 'data_load'

PLAY_SCENE = 'play_scene'
PLAY_CLIP = 'play_clip'
GLOBAL_STOP = 'global_stop'
STOP_CLIP = 'stop_clip'

LIST_DEVICES = 'list_device'
LIST_INSTRUMENTS = 'list_instrument'
LIST_TRACKS = 'list_track'
LIST_SCENES = 'list_scene'
LIST_CLIPS = 'list_clip'
LIST_PATTERNS = 'list_pattern'
LIST_TRANSFORMS = 'list_transform'
LIST_DATA_POOLS = 'list_data_pool'
LIST_SCALES = 'list_scale'

GET_SONG = 'get_song'
GET_DEVICE = 'get_device'
GET_INSTRUMENT = 'get_instrument'
GET_TRACK = 'get_track'
GET_SCENE = 'get_scene'
GET_CLIP = 'get_clip'
GET_PATTERN = 'get_pattern'
GET_TRANSFORM = 'get_transform'
GET_DATA_POOL = 'get_data_pool'
GET_SCALE = 'get_scale'

NEW_SONG = 'new_song'
NEW_DEVICE = 'new_device'
NEW_INSTRUMENT = 'new_instrument'
NEW_TRACK = 'new_track'
NEW_SCENE = 'new_scene'
NEW_CLIP = 'new_clip'
NEW_PATTERN = 'new_pattern'
NEW_TRANSFORM = 'new_transform'
NEW_DATA_POOL = 'new_data_pool'
NEW_SCALE = 'new_scale'

EDIT_SONG = 'edit_song'
EDIT_DEVICE = 'edit_device'
EDIT_INSTRUMENT = 'edit_instrument'
EDIT_TRACK = 'edit_track'
EDIT_SCENE = 'edit_scene'
EDIT_CLIP = 'edit_clip'
EDIT_PATTERN = 'edit_pattern'
EDIT_TRANSFORM = 'edit_transform'
EDIT_DATA_POOL = 'edit_data_pool'
EDIT_SCALE = 'edit_scale'

DELETE_INSTRUMENT = 'delete_instrument'
DELETE_TRACK = 'delete_track'
DELETE_SCENE = 'delete_scene'
DELETE_CLIP = 'delete_clip'
DELETE_PATTERN = 'delete_pattern'
DELETE_TRANSFORM = 'delete_transform'
DELETE_DATA_POOL = 'delete_data_pool'
DELETE_DEVICE = 'delete_device'
DELETE_SCALE = 'delete_scale'

REORDER_SCENE = 'reorder_scene'
REORDER_TRACK = 'reorder_track'

AUDITION_PATTERN = 'audition_pattern'
AUDITION_TRANSFORM = 'audition_transform'
AUDITION_STOP = 'audition_stop'

GET_PATTERN_GRID = 'grid_for_pattern'
GET_TRANSFORM_GRID = 'grid_for_transform'
GET_DATA_POOL_GRID = 'grid_for_data_pool'
GET_PATTERN_GRID_POSTBACK = 'grid_for_pattern_postback'
GET_TRANSFORM_GRID_POSTBACK = 'grid_for_transform_postback'
GET_DATA_POOL_GRID_POSTBACK = 'grid_for_data_pool_postback'

# ======================================================================================================================

class ApiRouter(object):

    __slots__ = ('api','callbacks','engine')

    def __init__(self, api, engine, callbacks=None):
        self.api = api
        self.callbacks = callbacks
        self.engine = engine

    # ------------------------------------------------------------------------------------------------------------------

    def dispatch(self, original_message, pkt):

        assert self.callbacks

        print("INCOMING PACKET: %s" % pkt.to_dict())

        try:

            # ----------------------------------------------------------------------------------------------------------
            # GENERAL/DEBUG


            if pkt.cmd == PLAY_SCENE:
                self.api.player.loop(pkt.name, abort=False, infinite=False)
                # after any START PLAY command we must be careful to not return a double response
                return None
            elif pkt.cmd == GLOBAL_STOP:
                self.api.player.user_called_stop()
                return ResponsePacket()

            elif pkt.cmd.startswith("list_"):
                return self.handle_lists(pkt)
            elif pkt.cmd.startswith("get_"):
                return self.handle_gets(pkt)
            elif pkt.cmd.startswith("edit_"):
                return self.handle_edits(pkt)
            elif pkt.cmd.startswith("new_"):
                return self.handle_new(pkt)
            elif pkt.cmd.startswith("reorder_"):
                return self.handle_reorder(pkt)
            elif pkt.cmd.startswith("delete_"):
                return self.handle_delete(pkt)
            elif pkt.cmd.startswith("audition_"):
                return self.handle_auditions(original_message, pkt)
            elif pkt.cmd.startswith('grid_for'):
                return self.handle_grids(pkt)
            elif pkt.cmd == HELLO:
                return ResponsePacket(msg='narf!')
            elif pkt.cmd.startswith("file_") or pkt.cmd.startswith("data_"):
                return self.handle_file_ops(pkt)
            else:
                raise InvalidOpcode()

        except Exception as e:

            traceback.print_exc()

            return ResponsePacket(ok=False, msg=str(e))

    # ------------------------------------------------------------------------------------------------------------------

    def handle_lists(self, pkt):
        data = None
        if pkt.cmd == LIST_DEVICES:
            data = self.api.devices.list()
        elif pkt.cmd == LIST_INSTRUMENTS:
            data = self.api.instruments.list()
        elif pkt.cmd == LIST_TRACKS:
            data = self.api.tracks.list(show_hidden=False)
        elif pkt.cmd == LIST_SCENES:
            data = self.api.scenes.list(show_hidden=False)
        elif pkt.cmd == LIST_CLIPS:
            data = self.api.clips.list()
        elif pkt.cmd == LIST_PATTERNS:
            data = self.api.patterns.list()
        elif pkt.cmd == LIST_TRANSFORMS:
            data = self.api.transforms.list()
        elif pkt.cmd == LIST_DATA_POOLS:
            data = self.api.data_pools.list()
        elif pkt.cmd == LIST_DEVICES:
            data = self.api.devices.list()
        elif pkt.cmd == LIST_SCALES:
            data = self.api.scales.list()
        else:
            raise InvalidOpcode()
        return ResponsePacket(data=data)

    # ------------------------------------------------------------------------------------------------------------------

    def handle_gets(self, pkt):

        # FIXME: add more types of objects here

        if pkt.cmd == GET_SONG:
            data = self.api.song.details()
        elif pkt.cmd == GET_DEVICE:
            data = self.api.devices.details(id=pkt.id)
        elif pkt.cmd == GET_SCENE:
            data = self.api.scenes.details(id=pkt.id)
        elif pkt.cmd == GET_SCALE:
            data = self.api.scales.details(id=pkt.id)
        elif pkt.cmd == GET_INSTRUMENT:
            data = self.api.instruments.details(id=pkt.id)
        elif pkt.cmd == GET_TRACK:
            data = self.api.tracks.details(id=pkt.id)
        elif pkt.cmd == GET_PATTERN:
            data = self.api.patterns.details(id=pkt.id)
        elif pkt.cmd == GET_TRANSFORM:
            data = self.api.transforms.details(id=pkt.id)
        elif pkt.cmd == GET_DATA_POOL:
            data = self.api.data_pools.details(id=pkt.id)
        elif pkt.cmd == GET_CLIP:
            data = self.api.clips.details(id=pkt.id)
        else:
            raise InvalidOpcode()

        data["choices"] = self.get_choices()

        return ResponsePacket(data=data)

    # ------------------------------------------------------------------------------------------------------------------

    def handle_grids(self, pkt):

        if pkt.cmd == GET_PATTERN_GRID_POSTBACK:
            data = self.api.patterns.update_web_slots_for_ui(id=pkt.id, data=pkt.data)
        elif pkt.cmd == GET_TRANSFORM_GRID_POSTBACK:
            raise Exception("???")
        if pkt.cmd == GET_PATTERN_GRID:
            data = self.api.patterns.get_web_slot_grid_for_ui(id=pkt.id, category=pkt.data['category'])
        elif pkt.cmd == GET_TRANSFORM_GRID:
            data = self.api.transform.get_web_slot_grid_for_ui(id=pkt.id, category=pkt.data['category'])
        elif pkt.cmd == GET_DATA_POOL_GRID:
            data = self.api.transform.get_web_slot_grid_for_ui(id=pkt.id, category=pkt.data['category'])
        return ResponsePacket(data=data)

    # ------------------------------------------------------------------------------------------------------------------

    def handle_delete(self, pkt):
        if pkt.cmd == DELETE_SCALE:
            self.api.scales.delete(id=pkt.id)
        elif pkt.cmd == DELETE_INSTRUMENT:
            self.api.instruments.delete(id=pkt.id)
        elif pkt.cmd == DELETE_SCENE:
            self.api.scenes.delete(id=pkt.id)
        elif pkt.cmd == DELETE_TRACK:
            self.api.tracks.delete(id=pkt.id)
        elif pkt.cmd == DELETE_PATTERN:
            self.api.patterns.delete(id=pkt.id)
        elif pkt.cmd == DELETE_TRANSFORM:
            self.api.transforms.delete(id=pkt.id)
        elif pkt.cmd == DELETE_DATA_POOL:
            self.api.data_pools.delete(id=pkt.id)
        elif pkt.cmd == DELETE_CLIP:
            self.api.clips.delete(id=pkt.id)
        else:
            raise InvalidOpcode()
        return ResponsePacket()

    # ------------------------------------------------------------------------------------------------------------------

    def handle_auditions(self, original_message, pkt):

        # FIXME: we should also handle the play code here!
        result = None
        if pkt.cmd == AUDITION_PATTERN:
            self.callbacks.startup_reply = original_message
            result = self.api.patterns.audition(id=pkt.id)
        elif pkt.cmd == AUDITION_TRANSFORM:
            self.callbacks.startup_reply = original_message
            result = self.api.transforms.audition(id=pkt.id)
        else:
            raise InvalidOpcode()
        # after any START PLAY command we must be careful to not return a double response
        if result is not None:
            # if we didn't start the event loop we must reply, else we don't!
            # any return code other than None from the above APIs indicates an error
            return ResponsePacket(ok=False)
        else:
            return None

    # ------------------------------------------------------------------------------------------------------------------

    def get_choices(self):
        return dict(
            scales = self.api.scales.list(),
            devices = self.api.devices.list(),
            instruments = self.api.instruments.list(),
            patterns = self.api.patterns.list(),
            notes = NOTES,
            scale_types = [ x for x in SCALE_TYPES.keys() ],
            scale_degrees = [x for x in SCALE_DEGREES_FOR_UI ],
        )

    # ------------------------------------------------------------------------------------------------------------------

    def handle_edits(self, pkt):
        if pkt.cmd == EDIT_SONG:
            self.api.song.edit(**pkt.data)
        elif pkt.cmd == EDIT_SCALE:
            self.api.scales.edit(**pkt.data)
        elif pkt.cmd == EDIT_INSTRUMENT:
            self.api.instruments.edit(**pkt.data)
        elif pkt.cmd == EDIT_SCENE:
            self.api.scenes.edit(**pkt.data)
        elif pkt.cmd == EDIT_TRACK:
            self.api.tracks.edit(**pkt.data)
        elif pkt.cmd == EDIT_PATTERN:
            self.api.patterns.edit(**pkt.data)
        elif pkt.cmd == EDIT_TRANSFORM:
            self.api.transforms.edit(**pkt.data)
        elif pkt.cmd == EDIT_DATA_POOL:
            self.api.data_pools.edit(**pkt.data)
        elif pkt.cmd == EDIT_CLIP:
            self.api.clips.edit(**pkt.data)
        else:
            raise InvalidOpcode(opcode=pkt.cmd)
        return ResponsePacket()

    # ------------------------------------------------------------------------------------------------------------------

    def handle_reorder(self, pkt):
        if pkt.cmd == REORDER_SCENE:
            self.api.scenes.reorder(**pkt.data)
        elif pkt.cmd == REORDER_TRACK:
            self.api.tracks.reorder(**pkt.data)
        else:
            raise InvalidOpcode(opcode=pkt.cmd)
        return ResponsePacket()

    # ------------------------------------------------------------------------------------------------------------------

    def handle_new(self, pkt):
        if pkt.cmd == NEW_SCALE:
            return ResponsePacket(data=self.api.scales.create())
        elif pkt.cmd == NEW_INSTRUMENT:
            return ResponsePacket(data=self.api.instruments.create())
        elif pkt.cmd == NEW_SCENE:
            return ResponsePacket(data=self.api.scenes.create())
        elif pkt.cmd == NEW_TRACK:
            return ResponsePacket(data=self.api.tracks.create())
        elif pkt.cmd == NEW_PATTERN:
            return ResponsePacket(data=self.api.patterns.create())
        elif pkt.cmd == NEW_TRANSFORM:
            return ResponsePacket(data=self.api.transforms.create())
        elif pkt.cmd == NEW_DATA_POOL:
            return ResponsePacket(data=self.api.data_pools.create())
        elif pkt.cmd == NEW_CLIP:
            raise Exception("this needs to take parameters!")
            return ResponsePacket(data=self.api.tracks.create())
        return InvalidOpcode(opcode=pkt.cmd)

    # ------------------------------------------------------------------------------------------------------------------

    def handle_file_ops(self, pkt):
        if pkt.cmd == FILE_NEW:
            self.api.reset()
            return ResponsePacket()
        elif pkt.cmd == DATA_LOAD:
            self.api.from_json(pkt.data["file_contents"])
            return ResponsePacket()
        elif pkt.cmd == FILE_SAVE:
            return ResponsePacket(data=self.api.to_dict())
        else:
            raise InvalidOpcode()