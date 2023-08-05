from warpseq.server import widgets

class BaseBuilder(object):

    @classmethod
    def build(cls, name, widgets, data, new=False):

        sf = widgets.smart_form(name=name, params=cls.get_form_parameters(data))
        bb = widgets.button_bar(params=cls.get_button_parameters(data))

        return dict(
            smart_form = sf,
            button_bar = bb,
            custom_js = cls.get_custom_js(),
        )

    @classmethod
    def get_form_parameters(cls, data):
        raise NotImplementedError()

    @classmethod
    def get_button_parameters(cls, data):
        raise NotImplementedError()

    @classmethod
    def get_custom_js(cls):
        return ""
