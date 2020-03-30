# Generated by Django 3.0.3 on 2020-03-06 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_product_families'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='families',
            new_name='categories',
        ),
        migrations.RemoveField(
            model_name='family',
            name='products',
        ),
        migrations.AddField(
            model_name='family',
            name='material',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Product'),
        ),
    ]
