from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=60)
    friendly_name = models.CharField(
        max_length=60, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    sku = models.CharField(max_length=60)
    category = models.ForeignKey(
        'Category', null=True, blank=True,
        on_delete=models.SET_NULL)
    style = models.CharField(max_length=60)
    color = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=250)
    price = models.DecimalField(
        max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=True, blank=True)
    item_count = models.IntegerField(
        blank=False, null=False, default=0)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=True, blank=True)

    def update_rating(self):
        print('here')
        self.rating = self.product_review.aggregate(Avg('rating'))['rating__avg'] or 0
        self.save()

    def __str__(self):
        return str(self.name)
