# Generated by Django 3.0.3 on 2020-02-26 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_product_refusine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='minQuantity',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
    ]