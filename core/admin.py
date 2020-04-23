from django.contrib import admin
from django.db import models
from .models import Profile, Entity, Affiliation
# Register your models here.


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    pass

@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class PersonAdmin(admin.ModelAdmin):
   pass
