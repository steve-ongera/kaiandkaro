# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split a string by the given argument"""
    return value.split(arg)

@register.filter
def range_filter(value):
    """Create a range from 0 to value"""
    return range(int(value))

@register.filter
def year_range(start, end=None):
    """Create a range of years"""
    if end is None:
        end = start + 10
    return range(int(start), int(end) + 1)