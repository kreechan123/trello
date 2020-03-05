from django.conf import settings
from django.conf.urls.static import static

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
    AddMemberView,
    UserConfirmationView,
    PostCommentView,
    DeleteComment,
    BoardDelete,
    RegisterView,
)


urlpatterns = [
    path('', LoginView.as_view(), name="index"),
    path('logout/',LogoutView.as_view(), name="logout"),
    path('signup/',RegisterView.as_view(), name="register"),
    
    path('boards/',DashBoardView.as_view(), name="dashboard"),
    path('board/<int:id>/', BoardDetailView.as_view(), name='detail'),
    path('board/<int:id>/lists/', BoardListView.as_view(), name='list'),
    path('card/<int:card_id>/detail/', CardDetail.as_view(), name='card_detail'),
    # Add
    path('board/<int:list_id>/addcard/', AddCard.as_view(), name='addcard'),
    path('board/<int:id>/addmember/', AddMemberView.as_view(), name='add_member'),
    path('card/<int:card_id>/upload/', CardUploadView.as_view(), name='card_upload'),
    path('card/<int:card_id>/comment/', PostCommentView.as_view(), name='post_comment'),
    path('card/<int:card_id>/pos/', CardPositionView.as_view(), name='card_position'),
    # Delete
    path('board/<int:board_id>/delete/board', BoardDelete.as_view(), name='delete_board'),
    path('board/<int:list_id>/delete/', DeleteList.as_view(), name='list_delete'),
    path('card/<int:card_id>/delete/', DeleteCard.as_view(), name='card_delete'),
    path('card/<int:comment_id>/comment/delete/', DeleteComment.as_view(), name='comment_delete'),

    # APIs
    path('board/<int:board_id>/lists/<int:list_id>/cards/', CardListView.as_view(), name='card'),
    path('card/<int:list_id>/edit/', ListUpdateView.as_view(), name='list_update'),
    path('card/<int:card_id>/des/', CardDescriptionView.as_view(), name='card_des'),

    path('confirm/<uuid:token>/<int:board_id>/', UserConfirmationView.as_view(), name='confirm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
