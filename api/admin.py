from django.contrib import admin
from .models import Person, Family, Product, ProductInstance, Organization, OrganizationType
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
    list_display = ('title', 'sku', 'family', 'location')
    inlines = [ProductInstanceInline]

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
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

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass