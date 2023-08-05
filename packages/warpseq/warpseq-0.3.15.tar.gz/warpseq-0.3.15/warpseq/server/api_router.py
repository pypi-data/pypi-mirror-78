# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# the api router decides what API calls to make for incoming
# service packet requests

from warpseq.server.packet import ResponsePacket
from warpseq.api.exceptions import InvalidOpcode
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
STOP = 'stop'
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

# ======================================================================================================================

class ApiRouter(object):

    __slots__ = ('api',)

    def __init__(self, api):
        self.api = api

    # ------------------------------------------------------------------------------------------------------------------

    def dispatch(self, pkt):

        print("INCOMING PACKET: %s" % pkt.to_dict())

        try:

            # ----------------------------------------------------------------------------------------------------------
            # GENERAL/DEBUG

            if pkt.cmd == HELLO:
                return ResponsePacket(msg='narf!')
            elif pkt.cmd.startswith("file_") or pkt.cmd.startswith("data_"):
                return self.handle_file_ops(pkt)
            elif pkt.cmd == PLAY_SCENE:
                self.api.player.loop(pkt.name)
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
            data = self.api.tracks.list()
        elif pkt.cmd == LIST_SCENES:
            data = self.api.scenes.list()
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
        else:
            raise InvalidOpcode()

        data["choices"] = self.get_choices()

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
        else:
            raise InvalidOpcode()
        return ResponsePacket()

    # ------------------------------------------------------------------------------------------------------------------

    def get_choices(self):
        return dict(
            scales = self.api.scales.list(),
            devices = self.api.devices.list(),
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