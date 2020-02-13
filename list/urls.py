from django.contrib import admin
from django.urls import path, include
from . import views
from list.views import LoginView, DashboardView


urlpatterns = [
    # path('',views.dashboard_view, name="dashboard_view"),
    path('', LoginView.as_view(), name="index"),
    path('boards/',DashboardView.as_view(), name="dashboard_view"),
    # path('b/<int:pk>',views.list_view, name="list_view"),
]
