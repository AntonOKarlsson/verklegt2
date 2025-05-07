from django.urls import path
from . import views
from .views import property_search

urlpatterns = [
    path('<int:id>/', views.get_property_by_id, name='property-by-id'),
    path('search', property_search, name='property-search'),
]
