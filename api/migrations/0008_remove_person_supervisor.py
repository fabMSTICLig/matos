# Generated by Django 3.0.3 on 2020-02-20 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_affiliation_organization_organizationtype_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='supervisor',
        ),
    ]