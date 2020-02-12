# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.

class Product(models.Model):
    sku = models.CharField(max_length=150,help_text="Enter Product Stock Keeping Unit")
    barcode = models.CharField(max_length=50,help_text="Enter Product Barcode (ISBN, UPC ...)")

    title = models.CharField(max_length=200, help_text="Enter Product Title")
    description = models.TextField(help_text="Enter Product Description")

    unitCost = models.FloatField(help_text="Enter Product Unit Cost")
    ##unit = models.CharField(max_length=10,help_text="Enter Product Unit ")

    quantity = models.FloatField(help_text="Enter Product Quantity")
    minQuantity = models.FloatField(help_text="Enter Product Min Quantity")

    family = models.ForeignKey('Family', models.CASCADE, blank=False, null = False)
    location = models.ForeignKey('Location', models.CASCADE, blank=False, null = False)

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Product.
        """
        return reverse('product-detail-view', args=[str(self.id)])

    def __str__(self):

        return self.title

class Family(models.Model):

    reference = models.CharField(max_length=150, help_text="Enter Family Reference")
    title = models.CharField(max_length=200, help_text="Enter Family Title")
    description = models.TextField(help_text="Enter Family Description")

    unit = models.CharField(max_length=40,help_text="Enter Family Unit ")

    minQuantity = models.FloatField(help_text="Enter Family Min Quantity")

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Family.
        """
        return reverse('family-detail-view', args=[str(self.id)])

    def __str__(self):

        return self.title

class Location(models.Model):

    reference = models.CharField(max_length=150, help_text="Enter Location Reference")
    title = models.CharField(max_length=200, help_text="Enter Location Title")
    description = models.TextField(help_text="Enter Location Description")

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Location.
        """
        return reverse('family-detail-view', args=[str(self.id)])

    def __str__(self):

        return self.title

class Transaction(models.Model):

    sku = models.CharField(max_length=130,help_text="Enter Product Stock Keeping Unit")
    barcode = models.CharField(max_length=50,help_text="Enter Product Barcode (ISBN, UPC ...)")

    comment = models.TextField(help_text="Enter Product Stock Keeping Unit", null=True, blank=True)

    unitCost = models.FloatField(help_text="Enter Product Unit Cost")

    quantity = models.FloatField(help_text="Enter Product Quantity")

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    date = models.DateField(null=True, blank=True)

    REASONS = (
        ('ns', 'New Stock'),
        ('ur', 'Usable Return'),
        ('nr', 'Unusable Return'),
        ('ul', 'Usable Lend')
    )


    reason = models.CharField(max_length=2, choices=REASONS, blank=True, default='ns', help_text='Reason for transaction')

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Product.
        """
        return reverse('transaction-detail-view', args=[str(self.id)])

    def __str__(self):

        return 'Transaction :  %d' % (self.id)

class User(models.Model):

    def __str__(self):
        return self.getChild().__str__()

    def getChild(self):
        try:
            return self.organization
        except (Organization.DoesNotExist):
            return self.person
            
    username = models.CharField(max_length=40)
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=250)


class OrganizationType(models.Model):
    """
    Type of organization (Labo,School, ...)
    """
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
            
class Organization(User):
    """
    Represent an Organization
    """
    name = models.CharField(max_length=30)
    contact = models.EmailField(max_length=100)
    orga_type = models.ForeignKey(
        OrganizationType, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name   
   
class Person(User):
    """
    Represent a person 
    It is automaticaly created when creating a user

    A ForeignKey with unique is used instead of a OneToOneField
    This choice was made to not be in conflict with the Inheritance OneToOneField

    organizations : [Organizations]
        Organizations to which the user belongs
    supervisor : bool
        True if the user can supervise a project
    charter : bool
        True if the user have signed the charter
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        unique=True,
        on_delete=models.CASCADE,
        related_name='person'
    )
    organizations = models.ManyToManyField(
        Organization, blank=True, related_name="members")
    supervisor = models.BooleanField(default=False)
    charter = models.BooleanField(default=False)

   
    def __str__(self):
        return self.user.username+"("+self.user.first_name+" "+self.user.last_name+")"
