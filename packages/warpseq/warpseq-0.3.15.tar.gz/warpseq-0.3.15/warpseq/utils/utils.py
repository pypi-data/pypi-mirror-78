# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# miscellaneous utility functions used throughout the program.

import random

def ensure_string_list(alist):
    if type(alist) == str:
        return alist.split()
    if type(alist) != list:
        return [ str(alist) ]
    return [ str(x) for x in alist ]

def roller(alist):
    """
    Returns a generator that keeps looping around a pattern
    """
    #return itertools.cycle(alist)

    if not alist:
         while True:
            yield None
    while True:
        for item in alist:
            yield item

def forever(item):
    while True:
        yield item

def index_where_exceeds(alist, item):
    index = None
    for (i, x) in enumerate(alist):
        if x >= item:
            index = i
            break
    return index

def reverse_roller(alist):

    alist = alist[:]
    alist.reverse()
    return roller(alist)

def oscillate_roller(alist):

    if not alist:
        while True:
            yield None

    blist = alist[:]
    blist.reverse()
    while True:
        for item in alist:
            yield item
        for item in blist:
            yield item

def pendulum_roller(alist):

    if not alist:
        while True:
            yield None

    blist = alist[:]
    blist.reverse()

    back_list = blist[0:-1]
    forward_list = alist[:-1]

    while True:
        for item in forward_list:
            yield item
        for item in back_list:
            yield item


def serialized_roller(alist):

    if not alist:
        while True:
            yield None


    blist = alist[:]
    random.shuffle(blist)

    while True:
        for item in blist:
            yield item
        random.shuffle(blist)

def random_roller(alist):

    if not alist:
        while True:
            yield None

    alist = alist[:]

    while True:
        yield random.choice(alist)

def build_roller(alist):

    if not alist:
        while True:
            yield None

    for x in alist:
        yield x

    while True:
        yield alist[-1]


def brownian1_roller(alist):
    return _generic_brownian_roller(alist, choices=[-1,1], walls_left=False, walls_right=False)

def brownian2_roller(alist):
    return _generic_brownian_roller(alist, choices = [-1,0,1], walls_left=False, walls_right=False)

def brownian3_roller(alist):
    return _generic_brownian_roller(alist, choices = [-1, 1], walls_left=True, walls_right=True)

def brownian4_roller(alist):
    return _generic_brownian_roller(alist, choices=[-1,0,1], walls_left=True, walls_right=True)

def brownian5_roller(alist):
    return _generic_brownian_roller(alist, choices=[-1,1], walls_left=True, walls_right=False)

def brownian6_roller(alist):
    return _generic_brownian_roller(alist, choices=[-1,0,1], walls_left=True, walls_right=False)

def _generic_brownian_roller(alist, choices=None, walls_left=True, walls_right=True):

    if not alist:
        while True:
            yield None

    index = int(random.random() * len(alist))

    while True:

        direction = random.choice(choices)
        index = index + direction
        length = len(alist)

        if index < 0:
            if walls_left:
                index = 0
            else:
                index = length - 1

        if index >= length:
            if walls_right:
                index = length - 1
            else:
                index = 0

        yield alist[index]
