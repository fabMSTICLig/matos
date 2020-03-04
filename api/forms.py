from django.forms import ModelForm
from api.models import Person, Affiliation, Organization
from django.db import models

class UserForm(ModelForm):
    class Meta:
        model = Person
        fields = ['username', 'email', 'firstname', 'lastname', 'affiliations']
    affiliations = models.ManyToManyField(Affiliation)

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['name','contact','affiliations']