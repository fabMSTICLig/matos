from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from .models import User, Entity, Affiliation, Tag, SpecificMaterial, GenericMaterial, SpecificMaterialInstance, Loan, LoanGenericItem
from django import forms

class CustomUserAdmin(UserAdmin):
    ...
    fieldsets = UserAdmin.fieldsets + (
        ('PlatPret', {'fields': ('is_pro', 'rgpd_accept','affiliations')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('PlatPret', {'fields': ('is_pro', 'rgpd_accept','affiliations',)}),
    )
    change_form_template = "admin/auth/user/change_form.html"
    change_list_template = "admin/auth/user/change_list.html"

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


class SpecificMaterialInstanceAdmin(admin.TabularInline):
    model = SpecificMaterialInstance

@admin.register(SpecificMaterial)
class SpecificMaterialAdmin(admin.ModelAdmin):
    model = SpecificMaterial
    inlines = [SpecificMaterialInstanceAdmin]


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
