# Generated by Django 3.0.3 on 2020-03-03 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_person_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='superuser',
            field=models.BooleanField(default=False),
        ),
    ]
