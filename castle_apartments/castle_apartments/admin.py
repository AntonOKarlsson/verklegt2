from django.contrib import admin
from offer.models import PurchaseOffer
from properties.models import Property



admin.site.register(PurchaseOffer)
admin.site.register(Property)