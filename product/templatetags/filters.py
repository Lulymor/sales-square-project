from django.template import Library
from utils import utils

register = Library()


@register.filter
def formatting_price(val):
    return utils.formatting_price(val)


@register.filter
def total_cart_qtd(cart):
    return utils.total_cart_qtd(cart)


@register.filter
def cart_total(cart):
    return utils.cart_total(cart)
