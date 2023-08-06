from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, button

CUSTOM_JS = """

function intercept_field(field,value) {
   if (field == 'slots') {
       clear_scale_type();
   } else if (field == 'scale_type') {
       clear_slots();
   }
   return true;
}

function edit_this() {
  edit_scale();
}
"""

class ScaleBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_button_parameters(cls, data):
        return None

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Name", "new_name"),
            select(data, "Root Note", "note", choices="notes"),
            select(data, "Scale Type", "scale_type", choices="scale_types", nullable=True),
            multiple(data, "Scale Degrees", "slots", choices="scale_degrees", nullable=True)
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS