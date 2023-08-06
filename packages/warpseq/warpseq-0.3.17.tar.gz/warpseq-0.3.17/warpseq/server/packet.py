import json

class BasePacket(object):

    __slots__ = ()

    def to_json(self):
        return json.dumps(self.to_dict())

class CommandPacket(BasePacket):

    __slots__ = ('cmd', 'name', 'id', 'data')

    def __init__(self, cmd=None, name=None, id=None, data=None):

        self.cmd = cmd
        self.name = name
        self.id = id
        self.data = data

    def to_dict(self):
        return dict(
            cmd = self.cmd,
            name = self.name,
            id = self.id,
            data = self.data
        )

    @classmethod
    def from_dict(cls, data):
        return CommandPacket(
            cmd = data.get("cmd"),
            name = data.get("name"),
            id = data.get("id"),
            data = data.get("data")
        )

class ResponsePacket(BasePacket):

    __slots__ = ( 'ok', 'msg', 'data', 'in_response_to' )

    def __init__(self, ok=True, msg=None, data=None, in_response_to=None):

        self.ok = ok
        self.msg = msg
        self.data = data
        self.in_response_to = data

    def to_dict(self):

        data = dict(
            ok = self.ok
        )

        if self.data is not None:
            data["data"] = self.data
        if self.msg is not None:
            data["msg"] = self.msg
        if self.in_response_to is not None:
            data["in_response_to"] = self.in_response_to

        return data

    @classmethod
    def from_dict(self, data):
        return ResponsePacket(
            ok = data.get('ok', None),
            data = data.get('data', None),
            msg = data.get('msg', None),
            in_response_to = data.get('in_response_to', None)
        )
