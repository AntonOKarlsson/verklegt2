from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile_images/')
    is_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Seller(models.Model):
    TYPE_PROPERITES = [('','Select type'),
                       ('real_estate','Real Estate agency'),
                       ('individual','Individual')]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    type = models.CharField(max_length=50, blank=True, choices=TYPE_PROPERITES)
    logo_url = models.TextField(blank=True)
    cover_image_url = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    agency_address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} (Seller)"

def create_seller(sender, instance, created, **kwargs):
    if created:
        seller_profile = Seller(user=instance)
        seller_profile.save()

post_save.connect(create_seller, sender=User)





