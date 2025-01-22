from django import template

register = template.Library()


@register.simple_tag
def active_class(request, url):
    return "active" if request.path == url else ""
