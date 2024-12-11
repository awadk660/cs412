# tell the admin we want to administer these models
from django.contrib import admin

from .models import * 
# Register your models here.

admin.site.register(Profile)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(Meal)