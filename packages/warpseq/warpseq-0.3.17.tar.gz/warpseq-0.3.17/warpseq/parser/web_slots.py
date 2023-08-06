# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.slot import Slot
from warpseq.model.evaluator import RandomRange, RandomChoice, Probability, DataGrab, LoadVariable

CATEGORY_COMMON = 'common'
CATEGORY_PITCH = 'pitch'
CATEGORY_TIME = 'time'
CATEGORY_MOD = 'modulation'
CATEGORY_CONTROL = 'control'

# column fields

INST_COMMON = [ "degree", "tie", "repeats", "length", "chord_type", "octave_shift", "velocity" ]
DRUM_COMMON = [ "note", "octave", "length", "repeats", "velocity" ]
INST_PITCH = [ "degree", "sharp", "flat", "chord_type", "degree_shift", "octave_shift" ]
DRUM_PITCH = [ "note", "octave" ]
TRANSFORM_PITCH = [ "degree_shift", "octave_shift", "sharp", "flat" ]
TIME = [ "length", "repeats", "delay", "rest" ]
MODULATION = [ "velocity", "cc_a", "cc_a_value", "cc_b", "cc_b_value", "cc_c", "cc_c_value" ]
CONTROL = [ "track_grab","shuffle", "reverse", "reset", "tie", "rest" ]

# header names for columns

HEADER_NAMES = {
   "degree": "Degree",
   "chord_type" : "Chord Type",
   "sharp" : "#",
   "flat" : "b",
   "degree_shift" : "Degree +/-",
   "octave_shift" : "Octave +/-",
   "note" : "Note",
   "octave" : "Octave",
   "length" : "Length",
   "repeats" : "Repeat",
   "delay" : "Delay",
   "rest" : "Rest",
   "velocity" : "Velocity",
   "cc_a" : "CC A",
   "cc_b": "CC B",
   "cc_c": "CC C",
   "cc_d": "CC D",
   "cc_a_value" : "=",
   "cc_b_value": "=",
   "cc_c_value": "=",
   "cc_d_value": "=",
   "shuffle" : "Shuffle",
   "reverse" : "Reverse",
   "reset" : "Reset",
   "tie" : "Tie",
   "track_grab" : "Track Grab"
}

ALL_COLUMNS =[x for x in HEADER_NAMES.keys() ]
INT_COLUMNS = [ "degree", "degree_shift", "octave_shift", "octave", "repeats", "velocity", "cc_a_value", "cc_b_value", "cc_c_value", "cc_d_value" "cc_a", "cc_b", "cc_c", "cc_d"]
FLOAT_COLUMNS = [ "length", "delay" ]
BOOL_COLUMNS = [ "sharp", "flat", "rest", "shuffle", "reverse", "reset", "tie" ]
STR_COLUMNS = [ "chord_type", "note", "track_grab" ]

# ======================================================================================================================


class WebSlotCompiler(object):

    __slots__ = ('for_transform', 'pattern_type')

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, for_transform=False, pattern_type=None):

        self.for_transform = for_transform
        self.pattern_type = pattern_type

    # ------------------------------------------------------------------------------------------------------------------

    def get_grid(self, web_slots, category):

        columns = self._get_columns_for_categories(category)
        return dict(
            column_defs = self._get_column_defs(columns),
            row_data = self._get_row_data(web_slots, columns)
        )

    # ------------------------------------------------------------------------------------------------------------------

    def _get_column_defs(self, columns):



        results = []

        results.append(dict(
            headerName = "slot",
            valueGetter = "node.rowIndex + 1"
        ))

        for x in columns:
            results.append(dict(
                headerName = HEADER_NAMES[x],
                field = x,
                editable = True,
            ))
        return results

    # ------------------------------------------------------------------------------------------------------------------

    def _get_row_data(self, web_slots, columns):

        results = []

        web_slot_items = web_slots
        if web_slot_items is None:
            web_slot_items = []



        for web_slot in web_slot_items:
            item = {}
            for column in columns:
                item[column] = web_slot.get(column, None)

            results.append(item)

        return results

    # ------------------------------------------------------------------------------------------------------------------

    def _get_columns_for_categories(self, category):

        # the web interface has switched to a different category and needs category headers

        from warpseq.model.pattern import PERCUSSION, STANDARD

        if category == CATEGORY_COMMON:
            if self.for_transform:
                return []
            elif self.pattern_type == PERCUSSION:
                return DRUM_COMMON
            else:
                return  INST_COMMON
        elif category == CATEGORY_PITCH:
            if self.for_transform:
                return TRANSFORM_PITCH
            elif self.pattern_type == PERCUSSION:
                return DRUM_PITCH
            else:
                return INST_PITCH
        elif category == CATEGORY_TIME:
            return TIME
        elif category == CATEGORY_MOD:
            return MODULATION
        elif category == CATEGORY_CONTROL:
            return CONTROL
        else:
            raise Exception("unknown category")

    # ------------------------------------------------------------------------------------------------------------------

    def update_web_slots_from_ui(self, web_slots, data):

        results = []

        existing_length = len(web_slots)

        for (i,x) in enumerate(data):
            if i < existing_length:
                item = web_slots[i]
            else:
                item = dict()
            item.update(x)
            results.append(item)

        new_length = len(data)
        if existing_length > new_length:
            results = results[:new_length-1]
        return results

    # ------------------------------------------------------------------------------------------------------------------

    def compile(self, web_slots):

        # FIXME: implement

        results = []
        errors = []

        for (i,x) in enumerate(web_slots):
            slot = Slot()

            for (k,v) in x.items():

                (ok, new_value) = self.parse_field(k, v, errors)
                if ok:
                    print("setattr to %s" % new_value)
                    setattr(slot, k, new_value)

            results.append(slot)


        if len(errors):
            return (False, results, errors)
        else:
            return (True, results, errors)

    # ------------------------------------------------------------------------------------------------------------------

    def parse_field(self, key, value, errors):

        value = str(value).strip()
        print("parsing value: %s" % value)

        if "," in value:
            choices = value.split(",")
            temp_results = [ self.parse_field(key, x, errors) for x in choices ]
            status = [ x[0] for x in temp_results ]
            values = [ x[1] for x in temp_results ]
            if False in status:
                return (False, None)
            else:
                return (True, RandomChoice(*values))

        if "-" in value and (key in INT_COLUMNS or key in FLOAT_COLUMNS):
            tokens = value.split('-')
            (left, right) = (tokens[0], tokens[1:])
            right = "-".join(right)
            (left_status, left_value) = self.parse_field(key, left, errors)
            (right_status, right_value) = self.parse_field(key, right, errors)
            if not left_status or not right_status:
                return (False, None)
            else:
                return (True, RandomRange(left_value, right_value))

        if value.startswith("@"):
            return (True, DataGrab(value[1:]))

        if value.startswith("$"):
            return (True, LoadVariable(value[1:]))

        if key in INT_COLUMNS:
            return self._parse_int_field(key, value, errors)
        elif key in BOOL_COLUMNS:
            return self._parse_bool_field(key, value, errors)
        elif key in STR_COLUMNS:
            return self._parse_str_field(key, value, errors)
        elif key in FLOAT_COLUMNS:
            return self._parse_float_field(key, value, errors)
        else:
            raise Exception("unknown key: %s" % key)

    # ------------------------------------------------------------------------------------------------------------------

    def _parse_int_field(self, key, value, errors):
        return (True, None)

    def _parse_bool_field(self, key, value, errors):
        # if the value is not 0 or 1 we need to return a probability of the value.
        return (True, None)

    def _parse_str_field(self, key, value, errors):
        return (True, None)

    def _parse_float_field(self, key, value, errors):
        return (True, None)



