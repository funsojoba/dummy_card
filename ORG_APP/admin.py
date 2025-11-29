from django.contrib import admin

from ORG_APP.models import OrganizationWallet, OrganzationTransaction


admin.site.register((OrganizationWallet, OrganzationTransaction))