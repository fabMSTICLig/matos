from django.contrib import admin
from django.db import models
from .models import Profile, Family, Product, ProductInstance, Organization, Affiliation
# Register your models here.
@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    pass

class ProductInstanceInline(admin.TabularInline):
    model = ProductInstance

class OrganizationInline(admin.TabularInline):
    model = Organization

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    categories = models.ManyToManyField(Family, limit_choices_to={'available': True})
    list_display = ('title', 'sku', 'categories', 'location')

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('product', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

@admin.register(Profile)
class PersonAdmin(admin.ModelAdmin):
   pass
