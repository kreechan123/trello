from django.contrib import admin
from django.urls import path, include
from . import views
from list.views import LoginView, DashboardView, LogoutView, BoardlistView, CardView

urlpatterns = [
    path('', LoginView.as_view(), name="index"),
    path('boards/',DashboardView.as_view(), name="dashboard_view"),
    path('logout/',LogoutView.as_view(), name="logout"),
    path('boards/<str:title>',BoardlistView.as_view(), name="list_view"),
    path('boards/<int:id>/modal/',CardView.as_view(), name="card_view"),
]
