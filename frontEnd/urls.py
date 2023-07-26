from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("create_marketplace", TemplateView.as_view(template_name="create_marketplace.html"), name='index'),
    path("dashboard/", TemplateView.as_view(template_name="dashboard.html"), name='dashboard'),
]