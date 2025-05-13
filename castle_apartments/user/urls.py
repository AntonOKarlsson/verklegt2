from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('createuser/', views.create_user, name='createuser'),
    path('updateuser/', views.update_user, name='updateuser'),
    path('updatepassword/', views.update_password, name='updatepassword'),
    path('updatesellerinfo/', views.update_sellerinfo, name='updatesellerinfo'),
    path('seller/<int:seller_id>/', views.seller_profile, name='seller-profile'),
    path('offers/', views.ListOfOffers.as_view(), name='list_of_offers'),
    path('offers/user/<int:user_id>/', views.ListOfOffers.as_view(), name='list_of_offers_by_user'),
    path('offers/finalize/<int:offer_id>/', views.get_offer_by_offer_id, name='finalize_offer'),
    path('offers/confirm/<int:offer_id>/', views.confirm_offer, name='confirm_offer'),
    path('offers/payment/<int:offer_id>/', views.payment_information, name='payment_information'),
    path('offers/creditcard/<int:offer_id>/', views.creditcard_information, name='creditcard_information'),
    path('offers/mortgage/<int:offer_id>/', views.mortgage_information, name='mortgage_information'),
    path('offers/confirmation/<int:offer_id>/', views.confirmation, name='confirmation'),
]
