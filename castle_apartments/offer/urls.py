from django.urls import path
from user import views

urlpatterns = [
    path('offers/update/<int:offer_id>/', views.update_offer_status, name='update_offer_status'),
    ]
