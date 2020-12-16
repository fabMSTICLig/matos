# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib import admin
# Create your models here.
from django.contrib.auth.models import AbstractUser

class Affiliation(models.Model):
    """
    Represent the institutinal affiliation of an entity
    ----------
    name : str
        Name of the institution
    type : str
        Type of the institution
    """
    name = models.CharField(max_length=50)
    TYPE_AFFILIATION = (
         ('Labo','Laboratoire'),
         ('Ecole','Ecole'),
         ('Platforme','Platforme'),
         ('Service','Service'),
         ('Recherche','Recherche'),
         ('Composante','Composante Universitaire')

    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_AFFILIATION,
        blank=True,
        default='',
        help_text='Type d\'affiliation',
    )

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom user model for the application
    ----------
    affiliations : Affiliation[]
        Institutional affiliations of the user
    rgpd_accpet : date
        Date at when the user has accepted the rgpd notice, null if not accpeted
    """
    affiliations = models.ManyToManyField(
        Affiliation, blank=True, related_name="members")
    rgpd_accept =  models.DateField(null=True, blank=True)
    def __str__(self):
        return self.username+"("+self.first_name+" "+self.last_name+")"

class Entity(models.Model):
    """
    Represent a lending entity
    It can be a school, a lab, a service, ....
    ----------
    name : str
        Name of the entity
    contact : email
        email to contact the entity
    description : str
        description of the entity
    affiliations : Affiliation[]
        Institutional affiliations of the entity
    managers : User[]
        managers of the entity
    """
    name = models.CharField(max_length=60, unique=True)
    contact = models.EmailField(max_length=100)
    managers = models.ManyToManyField(User,blank=True, related_name="entities")
    description = models.TextField(blank=True)
    affiliations = models.ManyToManyField(
        Affiliation, blank=True, related_name="entities")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "entities"

class Tag(models.Model):
    """
    Represent a tag used to help material search
    ----------
    name : str
        Name of the tag
    """
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Material(models.Model):
    """
    Abstract class for commom information beetween Generic and Specific material
    ----------
    name : str
        Name of the material
    description : str
        description of the material
    entity : Entity
        Entity owning of the material
    ref_int : str
        Reference intern at the entity of the material
    ref_man : str
        Reference of the manufacturer
    localisation : str
        localisation of the material Ex /Room33/Storage2/shelf3 (visible only to managers and admins)
    tags : Tag[]
        list of tag of the material (Ex, electronic, linux, arduino)
    """
    name = models.CharField(max_length=60)
    ref_int = models.CharField(max_length=50, null=True, blank=True)
    ref_man = models.CharField(max_length=50, null=True, blank=True)
    localisation = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="%(class)ss")
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="%(class)ss")
    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        unique_together = ['name', 'entity']

class GenericMaterial(Material):
    """
    Class for generic material most of the time small material
    ----------
    quantity : +int
        Quantity of the material 0 mean infinity
    """
    quantity = models.PositiveSmallIntegerField()

class SpecificMaterial(Material):
    """
    Class for specific material with a set of intances (material with serial number)
    ----------
    """
    pass

class SpecificMaterialInstance(models.Model):
    """
    Instance of specific material
    ----------
    name : str
        Name of the instance, can be an internal reference
    serial_num : str
        Serial number of the instance
    description : str
        description of the instance, can be use to note the state of wear
    model : SpecificMaterial
        material model of the instance
    """
    name = models.CharField(max_length=50)
    serial_num = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    model = models.ForeignKey(SpecificMaterial, on_delete=models.CASCADE, related_name="instances")
    def __str__(self):
        return self.model.name +"(" + self.name + ")"

    class Meta:
        unique_together = ['name', 'model']


class Loan(models.Model):
    class Status(models.IntegerChoices):
        REQUESTED = 2, 'Demandé'
        ACCEPTED = 3, 'Accepté'
        DENIED = 4, 'Refusé'
        CANCELED = 1, 'Annulé'

    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
    )
    checkout_date =  models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="loans")
    due_date =  models.DateField()
    return_date =  models.DateField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    specific_materials = models.ManyToManyField(
        SpecificMaterialInstance, blank=True, related_name="loans")
    generic_materials = models.ManyToManyField(
        GenericMaterial, blank=True, related_name="loans",through="LoanGenericItem")
    parent = models.OneToOneField('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="child")
    def __str__(self):
        return self.user.username +"(" + self.checkout_date.isoformat() + ")"

    def get_dict_specmat(self):
        dictmat = {}
        for specmat in self.specific_materials.all():
            if specmat.model not in dictmat:
                dictmat[specmat.model]=[]
            dictmat[specmat.model].append(specmat)
        print(dictmat)
        return dictmat


class LoanGenericItem(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    material = models.ForeignKey(GenericMaterial, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ['loan', 'material']
