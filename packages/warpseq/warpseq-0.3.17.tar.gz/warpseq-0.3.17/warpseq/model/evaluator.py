import random

VARIABLES = dict()

def set_variable(name, value):
    VARIABLES[name] = value

def evaluate(result, context, subject):
    if isinstance(result, Evaluator):
        return result.evaluate(context=context, subject=subject)
    return result

class Evaluator(object):

    __slots__ = ()

    SAVE_AS_REFERENCES = []

    def evaluate(self, context=None, subject=None):
        raise exceptions.NotImplementedError

    def is_hidden(self):
        # this is for the serializer which needs to exclude temporary scenes/tracks
        return False

class Probability(Evaluator):

    __slots__ = ('chance', 'a', 'b')

    SAVE_AS_REFERENCES = []

    def __init__(self, chance, a, b):
        self.chance = chance
        self.a = a
        self.b = b

    def evaluate(self, context=None, subject=None):

        chance = evaluate(self.chance, context, subject)

        if random.random() < chance:
            return evaluate(self.a, context, subject)
        else:
            return evaluate(self.b, context, subject)

class RandomChoice(Evaluator):

    __slots__ = ('values',)

    SAVE_AS_REFERENCES = []

    def __init__(self, *values):
        self.values = values
        super(RandomChoice, self).__init__()

    def evaluate(self, context=None, subject=None):
        options = [ evaluate(x, context, subject) for x in self.values ]
        res = random.choice(options)
        return res

class RandomRange(Evaluator):

    __slots__ = ('low','high')

    SAVE_AS_REFERENCES = []

    def __init__(self, low, high):
        self.low = low
        self.high = high
        super(RandomRange, self).__init__()

    def evaluate(self, context=None, subject=None):
        left = evaluate(self.low, context, subject)
        right = evaluate(self.high, context, subject)

        if left == right:
            return left

        if left > right:
            return left

        rng = random.randrange(left,right)
        return rng

class DataGrab(Evaluator):

    SAVE_AS_REFERENCES = []

    __slots__ = ('pool',)

    def __init__(self, pool):
        self.pool = pool
        super(DataGrab, self).__init__()

    def evaluate(self, context=None, subject=None):
        pool = context.song.find_data_pool_by_name(self.pool)
        if pool is None:
            return None
        data_slot = pool.get_next()
        value = data_slot.value
        res = evaluate(value, context, subject)
        return res


class LoadVariable(Evaluator):

    SAVE_AS_REFERENCES = []

    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name
        super(LoadVariable, self).__init__()

    def evaluate(self, context=None, subject=None):
        global VARIABLES
        gv = VARIABLES.get(self.name, 0)
        return gv

class Negate(Evaluator):

    SAVE_AS_REFERENCES = []

    __slots__ = ('what',)

    def __init__(self, what):
        self.what = what
        super(Negate, self).__init__()

    def evaluate(self, context=None, subject=None):
        result = 0 - evaluate(self.what, context, subject)
        return result




