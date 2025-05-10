from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_view, name='properties'),
    path('search/', views.property_search_page, name='property-search'),
    path('api/search/', views.json_search, name='property-search-api'),
    path('<int:id>/', views.get_property_by_id, name='property-by-id'),
    path('<int:id>/offer/', views.offer_on_property_by_id, name='offer-by-id'),
]