from django.contrib import admin
from .models import Property

# Register your models here.
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'postal_code', 'property_type')
    search_fields = ('title', 'address', 'postal_code')
    list_filter = ('property_type', 'built_year', 'seller')