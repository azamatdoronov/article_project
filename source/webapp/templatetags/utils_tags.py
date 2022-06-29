from django import template

register = template.Library()


@register.filter
def repeat(value, arg):
    return str(value) * arg