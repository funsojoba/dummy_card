from django.contrib import admin

from .models import Organization, APIToken, Member


admin.site.register((
    Organization, APIToken, Member
))
