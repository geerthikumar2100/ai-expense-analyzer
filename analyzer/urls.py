# analyzer/urls.py
from django.urls import path
from .views import dashboard_view

urlpatterns = [
    # Root URL will invoke dashboard_view
    path('', dashboard_view, name='dashboard'),
]
