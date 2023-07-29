from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("create_marketplace/", TemplateView.as_view(template_name="marketplaces/create_marketplace.html"), name='create-marketplace'),
    path("list_marketplace/", TemplateView.as_view(template_name="marketplaces/list_marketplaces.html"), name='list-marketplace'),
    path("dashboard/", TemplateView.as_view(template_name="dashboard.html"), name='dashboard'),
    path("create_brand/", TemplateView.as_view(template_name="brands/create_brands.html"), name='create-brand'),
    path("list_brands/", TemplateView.as_view(template_name="brands/list_brands.html"), name='list-brands'),
]