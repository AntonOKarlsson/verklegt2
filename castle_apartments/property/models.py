# models.py

from django.db import models

class Property(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.TextField()
    postal_code = models.CharField(max_length=10, blank=True)
    property_type = models.CharField(max_length=50, blank=True)
    num_rooms = models.IntegerField(null=True, blank=True)
    size_sqm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    built_year = models.IntegerField(null=True, blank=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
