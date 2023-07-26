from django.urls import path
from core import views

urlpatterns = [
    path('', views.index),
    path('add/',views.add_person),
    path('show/',views.get_all_person),
    path('create_marketplace_api/',views.create_marketplace_api),
]