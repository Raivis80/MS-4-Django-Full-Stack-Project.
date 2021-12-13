
from django.db import models
from django.conf import settings
from django.db.models import Sum
from django_countries.fields import CountryField

from django.contrib.auth.models import User
from customers.models import UserAddress
from shop.models import Product

import decimal


class Order(models.Model):
    SUBMITTED = 'Submitted'
    PROCESSED = 'Proccessed'
    SHIPPED = 'Shipped'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'

    ORDER_STATUS = [
        (SUBMITTED, 'Submittet'),
        (PROCESSED, 'Proccessed'),
        (SHIPPED, 'Shipped'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed'),
    ]

    # Order Info
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default=SUBMITTED, choices=ORDER_STATUS)
    order_number = models.CharField(max_length=32, null=False, editable=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    # User
    user_profile = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # User contact info
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    # Shipping Address
    shipping_name = models.CharField(max_length=50)
    shipping_address_1 = models.CharField(max_length=100)
    shipping_address_2 = models.CharField(max_length=100, null=True, blank=True)
    shipping_town = models.CharField(max_length=60)
    shipping_county = models.CharField(max_length=60, null=True, blank=True)
    shipping_postcode = models.CharField(max_length=30, null=True, blank=True)
    shipping_country = CountryField(blank_label='Country')

    # Shipping Address
    billing_name = models.CharField(max_length=50)
    billing_address_1 = models.CharField(max_length=100)
    billing_address_2 = models.CharField(max_length=100, null=True, blank=True)
    billing_town = models.CharField(max_length=60)
    billing_county = models.CharField(max_length=60, null=True, blank=True)
    billing_postcode = models.CharField(max_length=30, null=True, blank=True)
    billing_country = CountryField(blank_label='Country')

    def save(self, *args, **kwargs):
        """
        Update total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_number = str(self.id)
        self.count_total = self.lineitems.aggregate(Sum('product_total'))['product_total__sum'] or 0

        if self.count_total < 50:
            self.delivery = self.count_total * 10 / 100
            self.total = self.count_total + self.delivery
        else:
            self.delivery = 0
            self.total = self.count_total + self.delivery
        self.delivery = round(self.delivery, 2)
        self.total = round(self.total, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product_total = models.DecimalField(max_digits=6, decimal_places=2, editable=False, default=0)

    def save(self, *args, **kwargs):
        """
        and update the Product total.
        """
        if self.product.sale:
            self.product_total = self.product.sale_price * self.quantity
        else:
            self.product_total = self.product.price * self.quantity
        self.product_total = round(self.product_total, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
