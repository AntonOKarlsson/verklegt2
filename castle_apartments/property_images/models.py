from django.db import models
from properties.models import Property

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_photos/')
    is_thumbnail = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.property.title} ({'Thumbnail' if self.is_thumbnail else 'Gallery'})"
