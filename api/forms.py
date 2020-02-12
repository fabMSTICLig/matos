from django.forms import ModelForm
from api.models import User, Person, Organization
from django.db import models
from django.contrib.auth.models import User

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['username', 'email', 'firstname', 'lastname', 'organizations']
    organizations = models.ManyToManyField(Organization)

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['name','contact','orga_type']