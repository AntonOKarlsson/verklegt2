from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_view, name='properties'),
    path('properties/search/', views.search_properties, name='search-properties'),
    path('<int:id>/', views.get_property_by_id, name='property-by-id'),
    path('<int:id>/offer/', views.offer_on_property_by_id, name='offer-by-id'),
    path('add_property/', views.add_property2, name='property-add'),
    path('edit/<int:property_id>/', views.edit_property, name='edit_property'),
    path('set-thumbnail/<int:image_id>/', views.set_thumbnail, name='set_thumbnail'),
    ]