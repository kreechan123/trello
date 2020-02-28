from django import forms
from .models import Board, Boardlist, Card
from django.forms import Textarea

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)

class CreateBoardForm(forms.ModelForm):
        class Meta:
            model = Board
            fields = ('title',)

class AddListForm(forms.ModelForm):
        class Meta:
            model = Boardlist
            fields = ('title',)

class AddCardForm(forms.ModelForm):
        class Meta:
            model = Card
            fields = ('title',)
            widgets = {
            'title': Textarea(attrs={'cols': 24, 'rows': 0, 'placeholder':'Enter a title for this card...'}),
        }