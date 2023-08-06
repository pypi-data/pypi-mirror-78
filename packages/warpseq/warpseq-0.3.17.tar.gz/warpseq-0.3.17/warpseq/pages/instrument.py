from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, button, rangebox, toggle

CUSTOM_JS = """

function intercept_field(field,value) {
   return true;
}

function edit_this() {
  edit_instrument();
}
"""

CHANNELS = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']

class InstrumentBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_button_parameters(cls, data):
        return [
        ]

    # FIXME: should default 'device' to the first device

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Name", "new_name"),
            select(data, "Device", "device", choices="devices", nullable=True),
            select(data, "Channel", "channel", choices=CHANNELS, nullable=False),
            rangebox(data, "Min Octave", "min_octave", min=0, max=8, step=1, use_default=1),
            rangebox(data, "Base Octave", "base_octave", min=0, max=8, step=1, use_default=1),
            rangebox(data, "Max Octave", "max_octave", min=0, max=8, step=1, use_default=1),
            rangebox(data, "Default Velocity", "default_velocity", min=0, max=127, step=1, use_default=120),
            toggle(data, "Muted", "muted")
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS