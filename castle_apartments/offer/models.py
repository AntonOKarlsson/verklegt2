from django.contrib.auth.decorators import login_required
from django.db import models
from user.models import User
from properties.models import Property


class PurchaseOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('contingent', 'Contingent'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers', null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='offers')
    offer_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    # Add payment method to PurchaseOffer
    payment_method = models.CharField(max_length=50, null=True,
                                      blank=True)  # 'Credit Card', 'Mortgage', 'Bank Transfer'
    payment_submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        user_display = self.user.username if self.user else "Anonymous"
        return f"{user_display} - {self.property.title} - {self.status}"


class CreditCardInfo(models.Model):
    offer = models.OneToOneField(PurchaseOffer, on_delete=models.CASCADE, related_name='credit_card_info')
    card_token = models.CharField(max_length=100)
    last_four_digits = models.CharField(max_length=4)
    expiry_year = models.IntegerField()
    expiry_month = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)


class MortgageInfo(models.Model):
    offer = models.OneToOneField(PurchaseOffer, on_delete=models.CASCADE, related_name='mortgage_info')
    mortgage_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
