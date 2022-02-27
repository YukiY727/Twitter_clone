
from tempfile import template
from django.urls import path
from django.views.generic import TemplateView
from . import views
app_name = 'base'

urlpatterns = [
    path('', views.TopView.as_view(), name = 'top'),
]
