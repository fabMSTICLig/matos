from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from .models import User, Entity, Affiliation, SpecificMaterial, GenericMaterial, SpecificMaterialInstance


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

class SpecificMaterialInstanceAdmin(admin.TabularInline):
    model = SpecificMaterialInstance

@admin.register(SpecificMaterial)
class SpecificMaterialAdmin(admin.ModelAdmin):
    inlines = [SpecificMaterialInstanceAdmin]

@admin.register(GenericMaterial)
class GenericMaterialAdmin(admin.ModelAdmin):
    pass
