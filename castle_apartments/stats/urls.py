from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.index_plot, name='stats_home'),
]
