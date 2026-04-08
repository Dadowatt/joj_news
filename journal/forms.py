from django import forms

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Utilisateur, Commentaire

class Inscription(UserCreationForm):
    nom_complet = forms.CharField(
        label="Nom complet",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom complet'
        })
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })
    )

    class Meta:
        model = Utilisateur
        fields = ('username', 'nom_complet', 'email', 'password1', 'password2')

    # Transformation du nom_complet en first_name et last_name
    def save(self, commit=True):
        user = super().save(commit=False)
        nom_prenom = self.cleaned_data['nom_complet'].strip().split(' ', 1)
        user.first_name = nom_prenom[0]
        user.last_name = nom_prenom[1] if len(nom_prenom) > 1 else ''
        if commit:
            user.save()
        return user


class Connexion(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisatur"
        })
        )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        )


class CommentaireForm(forms.ModelForm):
    class Meta:
        model  = Commentaire
        fields = ["contenu"]
        widgets = {
            "contenu": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Partagez votre avis sur cet article…",
                "class": "form-control comment-textarea",
            })
        }
        labels = {"contenu": ""}
