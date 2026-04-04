from django.db import models
from django.contrib.auth.models import AbstractUser


class Utilisateur(AbstractUser):
    email = models.EmailField(unique=True)


class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Article(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    auteur = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    date_de_publication = models.DateTimeField(auto_now=True)