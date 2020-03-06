from django import forms
from .models import Board, Boardlist, Card, User
from django.forms import Textarea, TextInput, EmailInput, PasswordInput
from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.Form):
    
    username = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Enter username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Enter email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Firstname', 'autocomplete':"new-password"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Lastname', 'autocomplete':"new-password"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Enter password', 'autocomplete':"new-password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Confirm password', 'autocomplete':"new-password"}))
    # class Meta:
    #     model = User
    #     fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    #     help_texts = {
    #         'password': _('Must be 8-20 characters long'),
    #         'password2': _('Must be 8-20 characters long'),
    #     }

    #     widgets = {
    #         'username': TextInput(attrs={'class': 'form-control form-control-sm is_invalid', 'placeholder':'Enter username'}),
    #         'email': EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Enter email'}),
    #         'first_name': TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'First Name'}),
    #         'last_name': TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Last Name','autocomplete':"lastname"}),
    #         'password': PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Enter password', 'autocomplete':"new-password"}),
    #     }

    def save(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        fname = self.cleaned_data.get('first_name')
        lname = self.cleaned_data.get('last_name')

        user = User.objects.create_user(username, email, password)
        user.last_name = lname
        user.first_name = fname
        user.save()

        return user

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('password2')
        
        if pass1 != pass2:
            raise forms.ValidationError("Password did'nt match!")
        return pass2

    def clean_username(self):
        data = self.cleaned_data.get('username')
        user = User.objects.filter(username = data)
        if user.exists():
            raise forms.ValidationError("Username already exists")
        return data

    def clean_email(self):
        data = self.cleaned_data.get('email')
        email = User.objects.filter(email = data)
        if email.exists():
            raise forms.ValidationError("An account already registered with that email!")

        return data

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