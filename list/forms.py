from django import forms
from .models import Board

class LoginForm(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)

class CreateBoardForm(forms.ModelForm):
    # your_name = forms.CharField(label='Your name', max_length=100)
        class Meta:
            model = Board
            fields = ('title',)

