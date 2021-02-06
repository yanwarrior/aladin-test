from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Cart(models.Model):
    session_number = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='carts', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.BigIntegerField(default=0)
    total = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ('-created', '-updated')


class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    total = models.BigIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    customer_name = models.CharField(max_length=100, default='Dennis ivy')
    shipping_address = models.TextField(default='Jl. Jombang raya No. 56')

    def __str__(self):
        return self.order_number


class Item(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    price = models.BigIntegerField(default=0)
    total = models.BigIntegerField(default=0)

    def __str__(self):
        return self.product.name


