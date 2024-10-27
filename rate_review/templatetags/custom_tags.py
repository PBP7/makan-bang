from django import template

register = template.Library()

@register.filter
def to(value, end):
    return range(value, end + 1)


@register.filter
def floatmul(value, arg):
    """Multiplies the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
    
@register.filter
def has_decimal(value):
    """Returns True if the value has a decimal place."""
    return value % 1 != 0