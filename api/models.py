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

class OrganizationType(models.Model):
    """
    Type of organization (Labo,School, ...)
    """
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
            
class Affiliation(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=30)
    def __str__(self):
        return self.name


class Person(models.Model):

    username = models.CharField(max_length=40)
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=250)
    affiliations = models.ManyToManyField(
        Affiliation, blank=True, related_name="members")
    supervisor = models.BooleanField(default=False)

    def __str__(self):
        return self.username+"("+self.firstname+" "+self.lastname+")"


class Organization(models.Model):
    """
    an Organization
    """
    
    name = models.CharField(max_length=30)
    contact = models.EmailField(max_length=100)
    managed = models.ManyToManyField(Person,blank=False, related_name="managers")
    orga_type = models.ForeignKey(
        OrganizationType, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name   




   

class Reservation():
    """
    Represent a reservation
    ----------
    user : Person
        user making this reservation
    date : datetime
        Starting date and time of this reservation
    end_date : datetime
        Ending date and time of this reservation
    status : int
        Status of this reservation can be (Requested,Accepted,Denied,Changed)
    uses : [Equipment], 
        Equipment used for this reservation 
        (verified with the need of the reservation_type)
    created_date : datetime
        Time of creation of this reservation
    commentary : string, optional
        context of reservation or project linked in
    """
    REQUESTED = 1
    ACCEPTED = 2
    DENIED = 3
    CHANGED = 4
    STATUS = (
        (REQUESTED, ("Requested")),
        (ACCEPTED, ("Accepted")),
        (DENIED, ("Denied")),
        (CHANGED, ("Changed")),
    )
    status = models.SmallIntegerField(choices=STATUS, default=REQUESTED)
    end_date = models.DateTimeField()
    uses = models.ManyToManyField(Product, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    commentary = models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(
        Person, null=False, blank=False, on_delete=models.SET_NULL)
        
    def __str__(self):
        return self.user.__str__()+'('+str(self.date)+' '+str(self.end_date)+')'
