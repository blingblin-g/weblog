from django import template
from datetime import datetime

register = template.Library()

@register.filter
def datetime_format(value):
    if isinstance(value, datetime):
        return value.strftime("%Y. %m. %d. %H:%M:%S")
    return value 