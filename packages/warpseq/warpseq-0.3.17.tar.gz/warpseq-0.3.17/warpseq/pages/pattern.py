from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, button, rangebox, toggle, spacer
from warpseq.model.directions import DIRECTIONS
from warpseq.model.pattern import PATTERN_TYPES, STANDARD

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_pattern();
}

load_pattern_common_grid();

"""

class PatternBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Name", "new_name"),
            rangebox(data, "Octave shift", "octave_shift", min=-5, max=+5, use_default=0, step=1),
            textbox(data, "Rate", "rate"),
            select(data, "Scale", "scale", choices="scales", nullable=True),
            select(data, "Direction", "direction", choices=DIRECTIONS, nullable=False),
            select(data, "Pattern Type", "pattern_type", choices=PATTERN_TYPES, nullable=False),
            select(data, "Audition With", "audition_with", choices="instruments", nullable=True)
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return [
            button(caption="Copy", fa_icon="fa-copy", onclick="copy_this()"),
            button(caption="Audition", fa_icon="fa-play", onclick="audition_pattern()"),
            button(caption="Stop", fa_icon="fa-stop", onclick="global_stop()"),
        ]

    @classmethod
    def get_button2_parameters(self, data):
        return [
            button(caption="Common", fa_icon="fa-star", onclick="load_pattern_common_grid()"),
            button(caption="Pitch", fa_icon="fa-music", onclick="load_pattern_pitch_grid()"),
            button(caption="Time", fa_icon="fa-clock", fa_class="far", onclick="load_pattern_time_grid()"),
            button(caption="Mod", fa_icon="fa-random", onclick="load_pattern_modulation_grid()"),
            button(caption="Ctrl", fa_icon="fa-arrows-alt", fa_class="fas", onclick="load_pattern_control_grid()"),
            button(caption="(Add Row)", fa_icon="fa-plus", id="new_row_button"),
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS

    @classmethod
    def has_grid(self):
        return True