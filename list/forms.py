from django import forms
from .models import Board, Boardlist

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)

class CreateBoardForm(forms.ModelForm):
        class Meta:
            model = Board
            fields = ('title',)

class AddListForm(forms.ModelForm):
        class Meta:
            model = Boardlist
            fields = ('title',)
