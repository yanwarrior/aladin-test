from django import template

from ecommerce.models import Cart

register = template.Library()


@register.simple_tag
def total_carts(session_number):
    return Cart.objects.filter(session_number=session_number).count()