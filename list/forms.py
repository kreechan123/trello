from django import forms

class LoginForm(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
