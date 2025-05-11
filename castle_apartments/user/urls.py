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
]
