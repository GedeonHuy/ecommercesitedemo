from django import template

register = template.Library()

@register.filter(name='multiply_with')
def multiply_with(value, arg):
    return value*arg