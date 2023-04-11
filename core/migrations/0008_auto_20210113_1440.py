# Generated by Django 3.0.5 on 2021-01-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20201125_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericmaterial',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='specificmaterial',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='specificmaterialinstance',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]