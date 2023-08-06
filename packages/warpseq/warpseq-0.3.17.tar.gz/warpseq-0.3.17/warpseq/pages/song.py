from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, rangebox, button
from warpseq.model.scale import SCALE_TYPE_NAMES

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_song();
}
"""

class SongBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Name", "new_name"),
            textbox(data, "File name", "filename"),
            rangebox(data, "Tempo", "tempo", min=1, max=400, step=1, use_default=120),
            select(data, "Scale", "scale", choices="scales", nullable=True)
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return [
            button(caption="Open/Upload", fa_icon="fa-upload", onclick="file_load()"),
            button(caption="Save/Download", fa_icon="fa-download", onclick="file_save_as()"),
            button(caption="Erase/Initialize", danger=True, fa_class="far", fa_icon="fa-trash-alt", onclick="file_new()"),
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS