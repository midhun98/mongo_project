from django.urls import path, include
from core import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('marketplaces', views.MarketplaceViewSet, basename='career')

urlpatterns = [
    path('', views.index),
    path('add/', views.add_person),
    path('show/', views.get_all_person),
    path('api/', include(router.urls)),
]
