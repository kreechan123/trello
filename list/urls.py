from django.contrib import admin
from django.urls import path, include
from . import views
from list.views import LoginView, DashboardView, LogoutView, BoardlistView


urlpatterns = [
    path('', LoginView.as_view(), name="index"),
    path('boards/',DashboardView.as_view(), name="dashboard_view"),
    path('logouts/',LogoutView.as_view(), name="logout"),
    path('b/<int:pk>',BoardlistView.as_view(), name="list_view"),
]
