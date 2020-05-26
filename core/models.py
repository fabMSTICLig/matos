# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib import admin
import uuid # Required for unique book instances
# Create your models here.
from django.contrib.auth.models import AbstractUser

class Affiliation(models.Model):
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
    affiliations = models.ManyToManyField(
        Affiliation, blank=True, related_name="members")
    rgpd_accept =  models.DateField(null=True, blank=True)
    def __str__(self):
        return self.username+"("+self.first_name+" "+self.last_name+")"

class Entity(models.Model):
    """
    an Entity
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
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=30)
    ref_int = models.CharField(max_length=50, null=True, blank=True)
    ref_mat = models.CharField(max_length=50, null=True, blank=True)
    localisation = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="%(class)ss")
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="%(class)ss")
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class GenericMaterial(Material):
    quantity = models.PositiveSmallIntegerField()

class SpecificMaterial(Material):
    pass

class SpecificMaterialInstance(models.Model):
    name = models.CharField(max_length=30)
    ref_int = models.CharField(max_length=50, null=True, blank=True)
    serial_num = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    model = models.ForeignKey(SpecificMaterial, on_delete=models.CASCADE, related_name="instances")
    def __str__(self):
        return self.model.name +"(" + self.name + ")"
