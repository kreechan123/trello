from django.contrib import admin
from .models import Boardlist, Board, BoardMember, Card, Profile, Invite

admin.site.register(Boardlist)
admin.site.register(Board)
admin.site.register(BoardMember)
admin.site.register(Card)
admin.site.register(Profile)
admin.site.register(Invite)
