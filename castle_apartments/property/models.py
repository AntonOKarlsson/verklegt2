from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.TextField()
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    profile_image_url = models.TextField(blank=True)
    is_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, blank=True)
    logo_url = models.TextField(blank=True)
    cover_image_url = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    agency_address = models.TextField(blank=True)

    def __str__(self):
        return f"Seller: {self.user.username}"
