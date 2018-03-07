# from django.template.defaulttags import register
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get a value from a dict in templates"""
    return dictionary.get(key)