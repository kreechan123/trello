from django.contrib import admin
from .models import Boardlist, Board, BoardMember, Card, Profile

admin.site.register(Boardlist)
admin.site.register(Board)
admin.site.register(BoardMember)
admin.site.register(Card)
admin.site.register(Profile)
