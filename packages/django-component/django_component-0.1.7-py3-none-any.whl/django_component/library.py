from django import template
from .component import Component
from .component_tag import make_component_tag

import typing as t


class Library(template.Library):
    def __init__(self):
        super().__init__()

    def component(self, comp=None, name=None):
        def dec(comp: t.Type[Component]):
            component_name = name or comp.__name__
            self.tag(component_name, make_component_tag(comp, is_self_closed=False))
            self.tag(
                component_name + "/", make_component_tag(comp, is_self_closed=True)
            )
            return comp

        if comp is None:
            # @register.component(...)
            return dec
        elif issubclass(comp, Component):
            # @register.component
            return dec(comp)
        else:
            raise ValueError("Invalid arguments provided to component")
