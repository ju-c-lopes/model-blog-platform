from django import template

register = template.Library()


@register.filter
def replace_word(value):
    return value.replace(value[-2:], "ndo")
