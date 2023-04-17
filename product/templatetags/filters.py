from django.template import Library
from utils import utils

register = Library()


@register.filter
def formatting_price(val):
    return utils.formatting_price(val)
