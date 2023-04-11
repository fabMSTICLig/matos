# Generated by Django 4.1.7 on 2023-04-11 08:44

from django.db import migrations, models
import django.db.models.deletion
from django.contrib.auth import get_user_model
from django.conf import settings

def initial_is_pro(apps, schema):
    if(settings.ISPRO_SCHEMA):
        User = get_user_model()

        for u in User.objects.all():
            u.is_pro = u.email.endswith(tuple(settings.ISPRO_SCHEMA))
            u.save()

def reversal(*args):
    """Reversal is NOOP since is_pro is simply dropped during reverse"""

class Migration(migrations.Migration):

    replaces = [('core', '0010_user_is_pro_alter_genericmaterial_entity_and_more'), ('core', '0011_entity_is_pro')]

    dependencies = [
        ('core', '0009_auto_20211109_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_pro',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(initial_is_pro, reversal),
        migrations.AlterField(
            model_name='genericmaterial',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='core.entity'),
        ),
        migrations.AlterField(
            model_name='genericmaterial',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='%(class)ss', to='core.tag'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(2, 'En attente'), (3, 'Accepté'), (4, 'Refusé'), (1, 'Annulé')]),
        ),
        migrations.AlterField(
            model_name='specificmaterial',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='core.entity'),
        ),
        migrations.AlterField(
            model_name='specificmaterial',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='%(class)ss', to='core.tag'),
        ),
        migrations.AddField(
            model_name='entity',
            name='is_pro',
            field=models.BooleanField(default=False),
        ),
    ]