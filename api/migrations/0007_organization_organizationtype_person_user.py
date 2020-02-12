# Generated by Django 3.0.3 on 2020-02-10 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0006_auto_20200207_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('firstname', models.CharField(max_length=40)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.User')),
                ('name', models.CharField(max_length=30)),
                ('contact', models.EmailField(max_length=100)),
                ('orga_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.OrganizationType')),
            ],
            bases=('api.user',),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.User')),
                ('supervisor', models.BooleanField(default=False)),
                ('charter', models.BooleanField(default=False)),
                ('organizations', models.ManyToManyField(blank=True, related_name='members', to='api.Organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            bases=('api.user',),
        ),
    ]
