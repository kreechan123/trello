from django.contrib import admin
from django.urls import path, include
from . import views
from list.views import (
    LoginView,
    LogoutView,
    BoardDetailView,
    BoardListView,
    DashBoardView,
    CardListView,
    DeleteList,
    AddCard,
    CardDetail,
    DeleteCard,
    ListUpdateView,
    CardPositionView,
    CardDescriptionView,
    CardUploadView,
)
urlpatterns = [
    path('', LoginView.as_view(), name="index"),
    path('logout/',LogoutView.as_view(), name="logout"),
    
    path('boards/',DashBoardView.as_view(), name="dashboard"),
    path('board/<int:id>/', BoardDetailView.as_view(), name='detail'),

    # APIs
    path('board/<int:id>/lists/', BoardListView.as_view(), name='list'),
    path('board/<int:board_id>/lists/<int:list_id>/cards/', CardListView.as_view(), name='card'),
    path('board/<int:list_id>/delete/', DeleteList.as_view(), name='list_delete'),
    path('board/<int:list_id>/addcard/', AddCard.as_view(), name='addcard'),
    path('card/<int:card_id>/detail/', CardDetail.as_view(), name='card_detail'),
    path('card/<int:card_id>/delete/', DeleteCard.as_view(), name='card_delete'),
    path('card/<int:list_id>/edit/', ListUpdateView.as_view(), name='list_update'),
    path('card/<int:card_id>/pos/', CardPositionView.as_view(), name='card_position'),
    path('card/<int:card_id>/des/', CardDescriptionView.as_view(), name='card_des'),
    path('card/<int:card_id>/upload/', CardUploadView.as_view(), name='card_upload'),

]
