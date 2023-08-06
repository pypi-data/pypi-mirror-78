class Context(object):

    # where am I?

    __slots__ = ('song', 'clip', 'track', 'pattern', 'scene', 'player', 'track', 'scene', 'scale', 'base_length')

    def __init__(self, song=None, clip=None, pattern=None, player=None, track=None, scene=None, scale=None, base_length=None):

        self.song = song
        self.clip = clip
        self.track = track
        self.pattern = pattern
        self.scene = scene
        self.player = player
        self.track = track
        self.scene = scene
        self.scale = scale
        self.base_length = base_length