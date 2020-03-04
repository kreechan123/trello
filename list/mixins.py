from .models import Boardlist,Board,User, BoardMember
from django.http import Http404


class BoardPermissionMixin:

    def dispatch(self, *args, **kwargs):
        board_id = kwargs.get('id')
        user = self.request.user.id
        board = Board.objects.get(id=board_id)
        members = BoardMember.objects.filter(board=board)

        if members.filter(member = user).exists():
            return super().dispatch(self.request, *args, **kwargs)
        else:
            raise Http404


# class BoardPermissionMixin():

#     def dispatch(self, *args, **kwargs):
#         board_id

#         retriev all members sa board
#         if item in lists:

#         if user in Board member
#             return True
#         raise 404
