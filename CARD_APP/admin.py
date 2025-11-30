from django.contrib import admin

from CARD_APP.models import Card, Wallet, Transaction


admin.site.register((Card, Wallet, Transaction))
