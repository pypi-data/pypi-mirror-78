from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, button

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
}
"""

class DeviceBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
             textbox(data, "Name", "new_name", disabled=True)
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return None

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS