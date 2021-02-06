from django import forms
from django.forms import modelformset_factory

from ecommerce.models import Cart, Order


class CartCreateForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, max_value=100)


class CartUpdateForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity', ]


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name',
            'shipping_address',
        ]


class TrackOrderForm(forms.Form):
    order_number = forms.CharField()
