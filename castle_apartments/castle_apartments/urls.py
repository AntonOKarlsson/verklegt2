"""
URL configuration for castle_apartments project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import test_view, home
from properties.views import property_view
import user.views
from django.conf.urls.static import static
from django.conf import settings
from user.views import login_user, logout_user, seller_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_view, name='test'),
    path('properties/', include('properties.urls')),
    path('', home, name='home'),

    path('login/', user.views.login_user, name='login'),
    path('logout/', user.views.logout_user, name='logout'),
    path('createuser/', user.views.create_user, name='createuser'),
    path('updateuser/',user.views.update_user, name='updateuser'),
    path('updatepassword/',user.views.update_password, name='updatepassword'),

    path('seller/<int:seller_id>/', seller_profile, name='seller-profile'),
    path('updatesellerinfo/',user.views.update_sellerinfo, name='updatesellerinfo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)