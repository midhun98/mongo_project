from django.urls import path, include
from core import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('marketplaces', views.MarketplaceViewSet, basename='marketplaces')
router.register('brands', views.BrandsViewSet, basename='brands')
router.register('users', views.UserVieswet, basename='brands')

urlpatterns = [
    path('index/', views.index),
    path('api/', include(router.urls)),
]
