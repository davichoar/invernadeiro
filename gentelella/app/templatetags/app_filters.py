from django import template

register = template.Library()

@register.filter(name='haskey')
def haskey(value, arg):
    if arg in value:
        return True
    else:
        return False

@register.filter(name='get')
def get(value, arg):
    return value[arg]

@register.filter(name='idsemilla')
def idsemilla(value):
    return value.idsemilla