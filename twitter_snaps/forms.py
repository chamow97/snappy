from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        # widgets = {
        #     'username': forms.TextInput(attrs={'placeholder': 'Enter Username'}),
        #     'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        #     'email': forms.EmailInput(attrs={'placeholder': 'Enter E-Mail'})
        # }
        fields = ['username', 'email', 'password']