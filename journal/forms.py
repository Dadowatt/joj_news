from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Utilisateur


class Inscription(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True)

    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'password1', 'password2')

        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Email',
            'password1': 'Mot de passe',
            'password2': 'Confirmation',
        }


class Connexion(AuthenticationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Utilisateur
        fields = ('email', 'password1')

        labels = {
            'email': 'Email',
            'password1': 'Mot de passe', 
        }