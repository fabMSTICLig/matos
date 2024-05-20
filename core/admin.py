"""
Copyright (C) 2020-2024 LIG Université Grenoble Alpes


This file is part of Matos.

Matos is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
@author Clément Lesaulnier
@author Robin Courault
"""
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
