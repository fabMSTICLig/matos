from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from .models import User, Entity, Affiliation, Tag, SpecificMaterial, GenericMaterial, SpecificMaterialInstance, Loan, LoanGenericItem


class CustomUserAdmin(UserAdmin):
    ...
    fieldsets = UserAdmin.fieldsets + (
        ('PlatPret', {'fields': ('rgpd_accept','affiliations',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('PlatPret', {'fields': ('rgpd_accept','affiliations',)}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    pass

@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(SpecificMaterial)
class SpecificMaterialAdmin(admin.ModelAdmin):
    model = SpecificMaterial

@admin.register(GenericMaterial)
class GenericMaterialAdmin(admin.ModelAdmin):
    pass

class LoanGenericItemAdmin(admin.TabularInline):
    model = LoanGenericItem

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    model = Loan
    inlines = [LoanGenericItemAdmin]
    filter_horizontal  = ('specific_materials',)
