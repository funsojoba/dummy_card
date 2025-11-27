from django.contrib import admin

from .models import Organization, APIToken, Member, WebhookSettings


admin.site.register((
    Organization, APIToken, Member, WebhookSettings
))
