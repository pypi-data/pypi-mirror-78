from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, toggle, rangebox, button
from warpseq.model.track import INSTRUMENT_MODE_CHOICES

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_track();
}
"""

class TrackBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Name", "new_name"),
            toggle(data, "Muted", "muted"),
            multiple(data, "Instruments", "instruments", choices="instruments", nullable=True),
            select(data, "Instrument Mode", "instrument_mode", choices=INSTRUMENT_MODE_CHOICES, nullable=False),
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return None

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS