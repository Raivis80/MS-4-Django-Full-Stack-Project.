# Generated by Django 3.2.9 on 2021-12-14 12:15

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0002_remove_useraddress_phone'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Submitted', 'Submittet'), ('Proccessed', 'Proccessed'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed')], default='Submitted', max_length=50)),
                ('order_number', models.CharField(editable=False, max_length=32)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('delivery', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('items', models.TextField(default='')),
                ('stripe_pid', models.CharField(default='', max_length=254)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('shipping_name', models.CharField(max_length=50)),
                ('shipping_address_1', models.CharField(max_length=100)),
                ('shipping_address_2', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping_town', models.CharField(max_length=60)),
                ('shipping_county', models.CharField(blank=True, max_length=60, null=True)),
                ('shipping_postcode', models.CharField(blank=True, max_length=30, null=True)),
                ('shipping_country', django_countries.fields.CountryField(max_length=2)),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='customers.useraddress')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('product_total', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=6)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='checkout.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
    ]
