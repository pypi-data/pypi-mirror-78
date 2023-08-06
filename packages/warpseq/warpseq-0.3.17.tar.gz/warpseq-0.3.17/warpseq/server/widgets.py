# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

class Widgets(object):

    __slots__ = ('pages', 'templar')

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, pages=None, templar=None):
        self.pages = pages
        self.templar = templar

    # ------------------------------------------------------------------------------------------------------------------

    def select(self, choices=None, field=None, value=None, nullable=True, multiple=False):

        # deal with choices being a list of strings or objects...
        if len(choices) and type(choices[0]) == dict:
            choices = [x["name"] for x in choices]
        return self.templar.render('widgets/select.j2', locals())

    # ------------------------------------------------------------------------------------------------------------------

    def textbox(self, field=None, value=None, use_default=None, disabled=False):
        return self.templar.render('widgets/textbox.j2', locals())

    # ------------------------------------------------------------------------------------------------------------------

    def button(self, onclick="", fa_class="fas", fa_icon=None, aria_hidden=True, danger=False, caption=None, id=None, widget=None):
        assert caption is not None
        return self.templar.render('widgets/button.j2', locals())

    # ------------------------------------------------------------------------------------------------------------------

    def rangebox(self, field=None, value=None, min=None, max=None, step=None, use_default=None):
        return self.templar.render('widgets/rangebox.j2', locals())

    # ------------------------------------------------------------------------------------------------------------------

    def toggle(self, field=None, value=None):
        return self.templar.render('widgets/toggle.j2', locals())

    # ------------------------------------------------------------------------------------------------------------------

    def grid(self):
        return self.templar.render('widgets/grid.j2', locals())

    # ------------------------------------------------------------------------------------------------------------------

    def spacer(self, widget=None):
        return self.templar.render('widgets/spacer.j2', locals())

    # ------------------------------------------------------------------------------------------------------------------

    def button_bar(self, params=None):
        items = []
        for x in params:
            xcopy  = { k:v for (k,v) in x.items() }
            item = getattr(self, xcopy['widget'])(**xcopy)
            print("ITEM=>%s" % item)
            items.append(item)
        return self.templar.render('widgets/button_bar.j2', dict(items=items, widgets=self))

    # ------------------------------------------------------------------------------------------------------------------

    def smart_form(self, name=None, params=None):
        assert name is not None
        assert params is not None

        items = []

        selects = []
        textboxes = []
        ranges = []
        toggles = []

        for p in params:
            item = {}

            field = item['field'] = p["field"]
            item['caption'] = p['caption']
            widget = p['widget']


            if widget in [ 'textbox' ]:
                textboxes.append(field)
            if widget in [ 'select', 'multiple']:
                selects.append(field)
            if widget in [ 'rangebox' ]:
                ranges.append(field)
            if widget in [ 'toggle' ]:
                toggles.append(field)

            params_copy = { k:v for (k,v) in p.items() }
            del params_copy['caption']
            del params_copy['widget']

            print("widget params:" % params_copy)

            widget = getattr(self, widget)
            item['widget'] = widget(**params_copy)

            items.append(item)

        return self.templar.render('widgets/smart_form.j2', dict(items=items, widgets=self, name=name,
                selects=selects, textboxes=textboxes, ranges=ranges, toggles=toggles)
        )

#=======================================================================================================================
# parameter building shorcuts for smart_form and buttonbar, used to simply pages.py
# as opposed to the above class methods, these assume a bit about incoming data from the backend
# and apply convention to prevent redundant data entry

def textbox(data, caption, field, disabled=False, use_default=""):
    field_key = field
    if field == "new_name":
        field_key = "name"
    result = dict(caption=caption, field=field, widget="textbox", value=data.get(field_key,None), disabled=disabled, use_default=use_default)
    return result

def rangebox(data, caption, field, min=None, max=None, step=None, use_default=None):
    result = dict(caption=caption, field=field, widget="rangebox", value=data.get(field,0), min=min, max=max, step=step, use_default=use_default)
    return result

def select(data, caption, field, nullable=False, choices=None):
    result = dict(caption=caption, field=field, widget="select", value=data.get(field, None), nullable=nullable)
    if type(choices) == str:
        # ask the server!
        result["choices"] = data["choices"][choices]
    else:
        result["choices"] = choices

    return result

def multiple(data, caption, field, nullable=False, choices=None):
    result = dict(caption=caption, field=field, widget="select", value=data.get(field, None), nullable=nullable, multiple=True)
    if choices:
        result["choices"] = data["choices"][choices]
    return result

def button(caption=None, danger=False, fa_class="fas", fa_icon=None, onclick=None, id=None):
    return dict(caption=caption, danger=danger, widget="button", fa_class=fa_class, fa_icon=fa_icon, onclick=onclick, id=id)

def toggle(data, caption=None, field=None):
    return dict(caption=caption, widget='toggle', field=field, value=data[field])

def spacer():
    return dict(widget='spacer')