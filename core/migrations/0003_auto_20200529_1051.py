# Generated by Django 3.0.5 on 2020-05-29 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200519_2020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specificmaterialinstance',
            name='ref_int',
        ),
        migrations.AlterField(
            model_name='specificmaterialinstance',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]