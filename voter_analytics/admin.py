# voter_analytics/admin.py
# tell the admin we want to administer these models
from django.contrib import admin

from .models import * 

admin.site.register(Voter)
