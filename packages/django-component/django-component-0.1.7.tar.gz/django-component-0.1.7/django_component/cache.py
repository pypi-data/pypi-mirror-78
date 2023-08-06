from django.core.cache import InvalidCacheBackendError, caches
from django.core.cache.utils import make_template_fragment_key
from django.forms import Media
from django.template import (
    Node,
    TemplateSyntaxError,
    VariableDoesNotExist,
)

from django_component.arg_tag import ARGTAG_CONTEXT_KEY, merge_argtags
from django_component.media import MEDIA_CONTEXT_KEY, add_media


class CacheNode(Node):
    def __init__(self, nodelist, expire_time_var, fragment_name, vary_on, cache_name):
        self.nodelist = nodelist
        self.expire_time_var = expire_time_var
        self.fragment_name = fragment_name
        self.vary_on = vary_on
        self.cache_name = cache_name

    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError(
                '"cache" tag got an unknown variable: %r' % self.expire_time_var.var
            )
        try:
            expire_time = int(expire_time)
        except (ValueError, TypeError):
            raise TemplateSyntaxError(
                '"cache" tag got a non-integer timeout value: %r' % expire_time
            )
        if self.cache_name:
            try:
                cache_name = self.cache_name.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError(
                    '"cache" tag got an unknown variable: %r' % self.cache_name.var
                )
            try:
                fragment_cache = caches[cache_name]
            except InvalidCacheBackendError:
                raise TemplateSyntaxError(
                    "Invalid cache name specified for cache tag: %r" % cache_name
                )
        else:
            try:
                fragment_cache = caches["template_fragments"]
            except InvalidCacheBackendError:
                fragment_cache = caches["default"]

        vary_on = [var.resolve(context) for var in self.vary_on]
        cache_key = make_template_fragment_key(self.fragment_name, vary_on)
        cached = fragment_cache.get(cache_key)
        if cached is not None:
            value, media, argtags = cached
        else:
            with context.update({ARGTAG_CONTEXT_KEY: {}}):
                root_context = context.dicts[0]
                current_media = root_context.get(MEDIA_CONTEXT_KEY, Media())
                root_context[MEDIA_CONTEXT_KEY] = Media()
                value = self.nodelist.render(context)
                media = root_context[MEDIA_CONTEXT_KEY]
                root_context[MEDIA_CONTEXT_KEY] = current_media
                argtags = context[ARGTAG_CONTEXT_KEY]
            fragment_cache.set(cache_key, (value, media, argtags), expire_time)
        add_media(context, media)
        if argtags:
            merge_argtags(context[ARGTAG_CONTEXT_KEY], argtags)
        return value


def do_cache(parser, token):
    """
    This will cache the contents of a template fragment for a given amount
    of time.

    Usage::

        {% load cache %}
        {% cache [expire_time] [fragment_name] %}
            .. some expensive processing ..
        {% endcache %}

    This tag also supports varying by a list of arguments::

        {% load cache %}
        {% cache [expire_time] [fragment_name] [var1] [var2] .. %}
            .. some expensive processing ..
        {% endcache %}

    Optionally the cache to use may be specified thus::

        {% cache ....  using="cachename" %}

    Each unique set of arguments will result in a unique cache entry.
    """
    nodelist = parser.parse(("endcache",))
    parser.delete_first_token()
    tokens = token.split_contents()
    if len(tokens) < 3:
        raise TemplateSyntaxError("'%r' tag requires at least 2 arguments." % tokens[0])
    if len(tokens) > 3 and tokens[-1].startswith("using="):
        cache_name = parser.compile_filter(tokens[-1][len("using=") :])
        tokens = tokens[:-1]
    else:
        cache_name = None
    return CacheNode(
        nodelist,
        parser.compile_filter(tokens[1]),
        tokens[2],  # fragment_name can't be a variable.
        [parser.compile_filter(t) for t in tokens[3:]],
        cache_name,
    )
