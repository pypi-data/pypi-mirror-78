from warpseq.utils import utils
import random as random_module

FORWARD='forward'
REVERSE='reverse'
OSCILLATE='oscillate'
PENDULUM='pendulum'
RANDOM='random'
SERIALIZED='serialized'
BROWNIAN1='brownian1'
BROWNIAN2='brownian2'
BROWNIAN3='brownian3'
BROWNIAN4='brownian4'
BROWNIAN5='brownian5'
BROWNIAN6='brownian6'
BUILD='build'

DIRECTIONS = [
    FORWARD,
    REVERSE,
    OSCILLATE,
    PENDULUM,
    RANDOM,
    SERIALIZED,
    BROWNIAN1,
    BROWNIAN2,
    BROWNIAN3,
    BROWNIAN4,
    BROWNIAN5,
    BROWNIAN6,
    BUILD
]

DIRECTION_MAP = {
    FORWARD:    utils.roller,
    REVERSE:    utils.reverse_roller,
    OSCILLATE:  utils.oscillate_roller,
    PENDULUM:   utils.pendulum_roller,
    SERIALIZED: utils.serialized_roller,
    RANDOM:     utils.random_roller,
    BROWNIAN1:  utils.brownian1_roller,
    BROWNIAN2:  utils.brownian2_roller,
    BROWNIAN3:  utils.brownian3_roller,
    BROWNIAN4:  utils.brownian4_roller,
    BROWNIAN5:  utils.brownian5_roller,
    BROWNIAN6:  utils.brownian6_roller,
    BUILD:      utils.build_roller
}

class Directionable(object):

    __slots__ = ()

    def apply_direction(self):

        fn = DIRECTION_MAP.get(self.direction, None)
        if fn is not None:
            self._iterator = fn(self._current_slots)
        else:
            raise Exception("internal error: direction (%s) not implemented" % self.direction)

    def _get_slots(self):
        return self.slots[:]

    def reset(self):
        self._current_slots = self._get_slots()
        self.apply_direction()

    def shuffle(self):
        slots = self._current_slots[:]
        random_module.shuffle(slots)
        self._current_slots = slots
        self.apply_direction()

    def reverse(self):
        self._current_slots = [ x for x in reversed(self._current_slots) ]
        self.apply_direction()

    def get_next(self):
        res = next(self._iterator)
        return res