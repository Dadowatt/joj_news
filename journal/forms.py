from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Utilisateur, Commentaire
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Utilisateur


class Inscription(UserCreationForm):
    nom_complet = forms.CharField(
        label="Nom complet",
        required=True,
        help_text="Entrez votre prénom et nom"
    )
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = Utilisateur
        fields = ('username', 'nom_complet', 'email', 'password1', 'password2')

        labels = {
            'username': 'Nom d\'utilisateur',
            'password1': 'Mot de passe',
            'password2': 'Confirmation du mot de passe',
        }
    #transformation du nom_complet en first_name et last_name
    def save(self, commit=True):
        user = super().save(commit=False)
        nom_prenom = self.cleaned_data['nom_complet'].strip().split(' ', 1)
        user.first_name = nom_prenom[0]
        user.last_name = nom_prenom[1] if len(nom_prenom) > 1 else ''
        if commit:
            user.save()
        return user


class Connexion(AuthenticationForm):
    # Django utilise 'username' comme identifiant par défaut. 
    # On le renomme "Email" dans le label pour l'utilisateur.
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'})
    )
    # Le champ doit s'appeler 'password' (pas password1)
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'})
    )

    class Meta:
        model = Utilisateur
        fields = ('username', 'password')

 
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
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
