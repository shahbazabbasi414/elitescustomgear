
from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    return str(product.id) in cart

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    return cart.get(str(product.id), 0)


@register.filter
def get_cart_item(cart, product_id):
    return cart.get(str(product_id), {})
