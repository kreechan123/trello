from django.contrib import admin
from django.urls import path, include
from . import views
from list.views import (
    LoginView, 
    DashboardView, 
    LogoutView, 
    BoardlistView,
    CardView,

    BoardDetailView,
    BoardListView,
    DashBoardView,
    CardDetail,
    DeleteList,
    AddCard,
)
urlpatterns = [
    path('', LoginView.as_view(), name="index"),
    path('boards/',DashboardView.as_view(), name="dashboard_view"),
    path('logout/',LogoutView.as_view(), name="logout"),
    path('boards/<str:title>/',BoardlistView.as_view(), name="list_view"),
    path('boards/<int:id>/modal/',CardView.as_view(), name="card_view"),
    
    path('board/',DashBoardView.as_view(), name="dashboard"),
    path('board/<int:id>/', BoardDetailView.as_view(), name='detail'),

    # APIs
    path('board/<int:id>/lists/', BoardListView.as_view(), name='list'),
    path('board/<int:board_id>/lists/<int:list_id>/cards/', CardDetail.as_view(), name='card'),
    path('board/<int:list_id>/delete/', DeleteList.as_view(), name='list_delete'),
    path('board/<int:list_id>/addcard/', AddCard.as_view(), name='addcard'),

]
