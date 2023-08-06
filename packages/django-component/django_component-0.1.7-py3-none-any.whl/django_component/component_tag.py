from inspect import getfullargspec, unwrap

from django import VERSION as DJ_VERSION
from django import template
from django.template.library import parse_bits
from django.template import Context, NodeList

from .arg_tag import ArgNode, push_argtag_in_context, argtag_kwargs_from_context
from .component import Component
from .media import add_media

import typing as t


def make_component_tag(
    component_cls: t.Type[Component], is_self_closed: bool
) -> t.Callable:
    component = component_cls()
    [_, *params], varargs, varkw, defaults, kwonly, kwonly_defaults, _ = getfullargspec(
        unwrap(component.context)
    )

    def parse_component(parser, token) -> ComponentNode:
        component_name, *bits = token.split_contents()

        if DJ_VERSION[0] > 1:
            args, kwargs = parse_bits(
                parser,
                bits,
                params,
                varargs,
                varkw,
                defaults,
                kwonly,
                kwonly_defaults,
                False,
                component_name,
            )
        else:
            args, kwargs = parse_bits(
                parser, bits, params, varargs, varkw, defaults, False, component_name,
            )
        if is_self_closed:
            nodelist = NodeList()
        else:
            nodelist = parser.parse((f"/{component_name}",))
            parser.delete_first_token()

        return ComponentNode(component, nodelist, args, kwargs)

    return parse_component


class ComponentNode(template.Node):
    def __init__(
        self,
        component: Component,
        nodelist: template.NodeList,
        args: t.List,
        kwargs: t.Dict,
    ):
        self.component = component
        self.args = args
        self.kwargs = kwargs
        self.nodelist = nodelist

    def render(self, context: Context) -> str:
        self.register_media(context)
        args, kwargs = self.get_resolved_arguments(context)
        with context.push():
            context["children"], argtag_kwargs = self.render_between_tags(context)
            kwargs.update(argtag_kwargs)
            component_context = self.component.context(*args, **kwargs)
            with context.update(component_context):
                rendered = self.component.render(context)
        return rendered

    def render_between_tags(self, context):
        push_argtag_in_context(context)
        children = self.nodelist.render(context)
        argtag_kwargs = argtag_kwargs_from_context(context)
        return children, argtag_kwargs

    def register_media(self, context):
        add_media(context, self.component.media)

    def get_resolved_arguments(self, context):
        resolved_args = [var.resolve(context) for var in self.args]
        resolved_kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}
        return resolved_args, resolved_kwargs
