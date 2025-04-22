from django.urls import path
from .views import dashboard_view, delete_csv

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('delete/', delete_csv, name='delete_file'),
]
