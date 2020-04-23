# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib import admin
import uuid # Required for unique book instances
# Create your models here.
from django.contrib.auth.models import User


class Affiliation(models.Model):
    name = models.CharField(max_length=50)
    TYPE_AFFILIATION = (
         ('Labo','Laboratoire'), 
         ('Ecole','Ecole'),
         ('Platforme','Platforme')       
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


class Profile(models.Model):

    user =  models.OneToOneField(User, on_delete=models.CASCADE, blank=True,null=True)
    email = models.CharField(max_length=250)
    affiliations = models.ManyToManyField(
        Affiliation, blank=True, related_name="members")
    acceptance =  models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username+"("+self.user.first_name+" "+self.user.last_name+")"

class Entity(models.Model):
    """
    an Entity
    """
    
    name = models.CharField(max_length=60)
    contact = models.EmailField(max_length=100)
    managed = models.ManyToManyField(User,blank=True, related_name="managers")
    description = models.TextField(blank=True)
    affiliations = models.ManyToManyField(
        Affiliation, blank=True, related_name="entities")
    def __str__(self):
        return self.name   

