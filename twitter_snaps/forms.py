from django.contrib.auth.models import User
from django import forms
from django.forms import EmailField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            # 'password': forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
        }
        fields = ['username', 'email', 'password']

