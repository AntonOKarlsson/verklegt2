from django.contrib import admin
from .models import PropertyImage

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_thumbnail', 'image')
    list_filter = ('is_thumbnail',)
