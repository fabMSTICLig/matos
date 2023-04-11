# Generated by Django 3.1.3 on 2020-11-25 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20201030_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Demandé'), (3, 'Accepté'), (4, 'Refusé'), (1, 'Annulé')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]