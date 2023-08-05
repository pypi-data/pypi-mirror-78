import jinja2

from jinja2 import BaseLoader, TemplateNotFound
from os.path import join, exists, getmtime
import functools

# ======================================================================================================================

class CustomLoader(BaseLoader):

    # Jinja2 seemingly removed auto_reload=False, so built this...

    def __init__(self, path):
        self.path = path

    @functools.lru_cache()
    def get_source(self, environment, template):
        path = join(self.path, template)
        if not exists(path):
            raise TemplateNotFound(template)
        with open(path) as f:
            source = f.read()
        return source, path, lambda: True

# ======================================================================================================================

class Templar(object):

    __slots__ = ('jenv_strict',)

    def __init__(self, path):
        loader = CustomLoader(path)
        self.jenv_strict = jinja2.Environment(loader=loader, undefined=jinja2.StrictUndefined)

    def render(self, template, variables):
        template = self.jenv_strict.get_template(template)
        return template.render(variables)

    def register(self, key, value):
        self.jenv_strict.globals[key] = value;
