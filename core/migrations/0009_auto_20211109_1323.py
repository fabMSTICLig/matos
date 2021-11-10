# Generated by Django 3.2 on 2021-11-09 12:23

from django.db import migrations, models
import django.db.models.deletion

def setAffDefault(apps, schema_editor):
    Loan = apps.get_model("core", "Loan")
    db_alias = schema_editor.connection.alias
    for loan in Loan.objects.using(db_alias).all():
        if (loan.user.affiliations.first()):
            loan.affiliation=loan.user.affiliations.first()
            loan.save()
def empty(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210113_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='affiliation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loans', to='core.affiliation'),
        ),
        migrations.RunPython(setAffDefault, empty),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
