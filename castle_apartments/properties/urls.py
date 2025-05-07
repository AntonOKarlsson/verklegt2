from django.urls import path
from . import views
from .views import property_search

urlpatterns = [
    path('<int:id>/', views.get_property_by_id, name='property-by-id'),
    path('search/', property_search, name='properties/search'),
    path('api/search/', views.json_search, name='property-json-search'),
    path('search-page/', views.property_search_page, name='property-search-page'),
]
