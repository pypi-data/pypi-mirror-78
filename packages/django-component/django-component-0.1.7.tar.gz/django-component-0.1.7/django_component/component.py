from django.forms.widgets import MediaDefiningClass
from django.template import Context


class Component(metaclass=MediaDefiningClass):
    template: str = ""

    def context(self, *args, **kwargs):
        return kwargs

    def render(self, context: Context) -> str:
        template = context.template.engine.get_template(self.template)
        return template.render(context)
