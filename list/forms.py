from django import forms
from .models import Board, Boardlist, Card, User
from django.forms import Textarea, TextInput, EmailInput, PasswordInput
from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        labels = {
            'username': _('username'),
            'email': _('email'),
            'first_name': _('first_name'),
            'last_name': _('last_name'),
            'password': _('password'),
        }
        help_texts = {
            'password': _('Must be 8-20 characters long'),
        }
        error_messages = {
            'username': {
                'blank': _("Username field is required"),
            },
        }
        widgets = {
            'username': TextInput(attrs={'class': 'form-control form-control-sm is_invalid', 'placeholder':'Enter username'}),
            'email': EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Enter email'}),
            'first_name': TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'First Name'}),
            'last_name': TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Last Name','autocomplete':"lastname"}),
            'password': PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Enter password', 'autocomplete':"new-password"}),
        }

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
            widgets = {
            'title': TextInput(attrs={'cols': 24, 'rows': 0, 'placeholder':'Enter list title ...', 'data-toggle':'popover'}),
        }

class AddCardForm(forms.ModelForm):
        class Meta:
            model = Card
            fields = ('title',)
            widgets = {
            'title': Textarea(attrs={'cols': 24, 'rows': 0, 'placeholder':'Enter a title for this card...'}),
        }