from django.template import Library
from django_component.arg_tag import arg_tag
from django_component.media import media_tag
from django_component.cache import do_cache

register = Library()

register.tag("arg", arg_tag)
register.tag("components_css", media_tag("css"))
register.tag("components_js", media_tag("js"))
register.tag("cache", do_cache)
