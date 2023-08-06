from warpseq.server import widgets

class BaseBuilder(object):

    @classmethod
    def build(cls, name, widgets, data, new=False):

        sf = widgets.smart_form(name=name, params=cls.get_form_parameters(data))

        bb1p = cls.get_button_parameters(data)
        bb2p = cls.get_button2_parameters(data)

        bb = None
        bb2 = None

        if bb1p:
            bb = widgets.button_bar(params=bb1p)
        if bb2p:
            bb2 = widgets.button_bar(params=bb2p)

        return dict(
            smart_form = sf,
            button_bar = bb,
            custom_js = cls.get_custom_js(),
            button_bar2 = bb2,
        )

    @classmethod
    def get_form_parameters(cls, data):
        raise NotImplementedError()

    @classmethod
    def get_button_parameters(cls, data):
        return None

    @classmethod
    def get_button2_parameters(cls, data):
        return None

    @classmethod
    def get_custom_js(cls):
        return ""

    @classmethod
    def has_grid(self):
        return False
