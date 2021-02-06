from django.urls import path

from ecommerce import views

app_name = 'ecommerce'


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('carts/', views.cart_list, name='cart_list'),
    path('carts/reset', views.cart_reset, name='cart_reset'),
    path('carts/<int:product_id>/', views.cart_create, name='cart_create'),
    path('carts/<int:cart_id>/edit/', views.cart_edit, name='cart_edit'),
    path('carts/<int:cart_id>/delete/', views.cart_delete, name='cart_delete'),
    path('orders/checkout/', views.order_create, name='order_create'),
    path('orders/track/', views.order_track, name='order_track'),
]