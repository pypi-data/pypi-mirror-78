from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, rangebox, button, toggle
from warpseq.model.transform import APPLIES_CHOICES
from warpseq.model.directions import DIRECTIONS

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_transform();
}
"""

DIVIDE = [ "auto", "1", "2", "3", "4", "5", "6", "7", "8" ]

class TransformBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Name", "new_name"),
            toggle(data, "Arpeggiate", "arp"),
            select(data, "Divide", "divide", choices=DIVIDE, nullable=True),
            select(data, "Applies To", "applies_to", choices=APPLIES_CHOICES),
            select(data, "Direction", "direction", choices=DIRECTIONS, nullable=False),
            toggle(data, "Auto Reset", "auto_reset"),
            select(data, "Audition Instrument", "audition_instrument", choices="instruments", nullable=True),
            select(data, "Audition Pattern", "audition_pattern", choices="patterns", nullable=True),

        ]

    @classmethod
    def get_button_parameters(cls, data):
        return [
            button(caption="Audition", fa_icon="fa-play", onclick="audition_transform()"),
            button(caption="Stop", fa_icon="fa-stop", onclick="global_stop()"),
            button(caption="Copy", fa_icon="fa-copy", onclick="copy_this()"),
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS

    @classmethod
    def has_grid(self):
        return True