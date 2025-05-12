# models.py

from django.db import models

class Property(models.Model):
    seller = models.ForeignKey('user.Seller', on_delete=models.CASCADE, related_name='properties')
    header_image = models.ImageField(upload_to='media/property_images/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.TextField()
    postal_code = models.CharField(max_length=10, blank=True)
    property_type = models.CharField(max_length=50, blank=True)
    num_rooms = models.IntegerField(null=True, blank=True)
    num_bedrooms = models.IntegerField(null=True, blank=True)
    num_bathrooms = models.IntegerField(null=True, blank=True)
    size_sqm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    built_year = models.IntegerField(null=True, blank=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def thumbnail_image(self):
        return self.images.filter(is_thumbnail=True).first()

    def __str__(self):
        return self.title

class PostalCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    label = models.CharField(max_length=100, blank=True, null=True)  # optional district

    @property
    def subgroup(self):
        return self.city if self.city == "Reykjavík" else self.region

    def __str__(self):
        base = f"{self.code} {self.city}"
        if self.label:
            base += f" — {self.label}"
        return base