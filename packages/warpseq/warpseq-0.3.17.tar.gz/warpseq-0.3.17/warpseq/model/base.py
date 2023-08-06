# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# base classes for model objects

from warpseq.utils.serialization import save_object, load_object

COUNTER = 0

class BaseObject(object):

    __slots__ = ()

    def one(self, alist):
        length = len(alist)
        if length == 0:
            return None
        assert length == 1
        return alist[0]

    def is_hidden(self):
        return False

class NewReferenceObject(BaseObject):

    __slots__ = ( 'obj_id' )

    @classmethod
    def new_object_id(cls):
        global COUNTER
        COUNTER = COUNTER + 1
        return str(COUNTER)

    def __init__(self):
        if self.obj_id in [ None, '0' ]:
            self.obj_id = NewReferenceObject.new_object_id()

    def to_dict(self):
        return save_object(self)

    @classmethod
    def from_dict(cls, song, data):
        return load_object(song, data)
