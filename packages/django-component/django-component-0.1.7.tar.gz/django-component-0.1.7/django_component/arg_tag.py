from django import template

ARGTAG_CONTEXT_KEY = "__django_component__arg_tag"


def arg_tag(parser, token):
    [arg_tag_name] = token.split_contents()[1:]
    nodelist = parser.parse(("endarg",))
    parser.delete_first_token()
    return ArgNode(arg_tag_name, nodelist)


def push_argtag_in_context(context):
    context[ARGTAG_CONTEXT_KEY] = {}


def argtag_kwargs_from_context(context):
    return context[ARGTAG_CONTEXT_KEY]


def add_argtag(argtags, key, rendered):
    if key in argtags:
        if not isinstance(argtags[key], list):
            argtags[key] = [argtags[key]]
        argtags[key].append(rendered)
    else:
        argtags[key] = rendered


def merge_argtags(argtags_1, argtags_2):
    """ Merge argtags_2 into argtags_1 """
    for key, value in argtags_2.items():
        if isinstance(value, list):
            for v in value:
                add_argtag(argtags_1, key, v)
        else:
            add_argtag(argtags_1, key, value)


class ArgNode(template.Node):
    def __init__(self, key, nodelist):
        self.key = key
        self.nodelist = nodelist

    def render(self, context):
        rendered = self.nodelist.render(context)
        argtags = context[ARGTAG_CONTEXT_KEY]
        add_argtag(argtags, self.key, rendered)
        return ""
