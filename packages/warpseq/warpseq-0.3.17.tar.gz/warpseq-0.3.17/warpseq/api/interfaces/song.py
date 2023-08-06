# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

import json

class SongApi(object):

    def __init__(self, public_api, song):
        self.public_api = public_api
        self.song = song

    def edit(self, name:str=None, new_name:str=None, id:str=None, filename:str=None, tempo:int=None, scale:str=None):
        # id is ignored, because there is only one song.
        if tempo:
            self.song.tempo = int(tempo)
        if scale:
            scale = self.public_api.scales.lookup(scale, require=True, field="scale")
            self.song.scale = scale
        if name:
            self.song.name = name
        if new_name:
            # just provided to be consistent with other object edit commands
            self.song.name = new_name
        if filename:
            self.song.filename = filename

    def details(self):
        return self.song.details()

    def to_dict(self):
        return self.song.to_dict()

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)