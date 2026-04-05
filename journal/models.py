from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings 

class Utilisateur(AbstractUser):
    email = models.EmailField(unique=True)


class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Article(models.Model):
    titre       = models.CharField(max_length=255)
    categorie   = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles")
    contenu     = models.TextField()
    resume      = models.CharField(max_length=400, blank=True, help_text="Court résumé affiché dans les cartes")
    image       = models.ImageField(upload_to="articles/", blank=True, null=True)
    auteur      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now=True)
    date_modification = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"
 
    def __str__(self):
        return self.titre
 
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})
 
class Commentaire(models.Model):
    article       = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="commentaires")
    auteur        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="commentaires")
    contenu       = models.TextField(verbose_name="Votre commentaire")
    date_creation = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ["date_creation"]
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
 
    def __str__(self):
        return f"Commentaire de {self.auteur.username} sur « {self.article.titre} »"
