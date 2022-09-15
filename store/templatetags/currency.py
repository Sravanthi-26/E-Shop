#from atexit import register
from django import template

register = template.Library()


@register.filter(name = 'indian_currency')
def indian_currency(amount):
    return '₹ '+str(amount)
    