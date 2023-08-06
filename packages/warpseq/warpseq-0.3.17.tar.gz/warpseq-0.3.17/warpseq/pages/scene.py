from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, toggle, rangebox, button

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_scene();
}
"""

class SceneBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Name", "new_name"),
            textbox(data, "Rate", "rate"),
            toggle(data, "Auto Advance", "auto_advance"),
            select(data, "Scale", "scale", choices="scales", nullable=True)
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return None

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS