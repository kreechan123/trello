from .models import Boardlist,Board,User, BoardMember
from django.http import Http404


class BoardPermissionMixin:

    def dispatch(self, *args, **kwargs):
        board_id = kwargs.get('id')
        board = Board.objects.get(id=board_id)
        members = BoardMember.objects.filter(board=board, member=self.request.user)

        if members.exists():
            return super().dispatch(self.request, *args, **kwargs)
        raise Http404