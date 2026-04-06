from django.shortcuts import redirect
from django.views.generic import CreateView,ListView, DetailView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import Inscription, Connexion
from .models import Article
from .forms import CommentaireForm
from django.contrib import messages


class Inscription(CreateView):
    form_class = Inscription
    success_url = reverse_lazy('connexion')
    template_name = 'registration/inscription.html'

class Connexion(LoginView):
    form_class = Connexion
    template_name = 'registration/connexion.html'
    success_url = reverse_lazy('home')


# PAGE D'ACCUEIL (LISTE DES ARTICLES)

class ArticleListView(ListView):
    model = Article
    template_name = "index.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        """
        Récupère tous les articles avec leurs relations
        pour éviter les requêtes multiples (optimisation).
        """
        articles = Article.objects.select_related("categorie", "auteur").all()
        return articles

    def get_context_data(self, **kwargs):
        """
        Ajoute des données supplémentaires pour le template.
        """
        context = super().get_context_data(**kwargs)

        articles = self.get_queryset()

        # Articles pour le carrousel (les 4 premiers)
        context["hero_articles"] = articles[:4]

        # Articles pour la grille (les suivants)
        context["grid_articles"] = articles[4:9]

        return context



# PAGE DÉTAIL D’UN ARTICLE + COMMENTAIRES

class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        """
        Envoie toutes les données nécessaires à la page détail.
        """
        context = super().get_context_data(**kwargs)

        article = self.get_object()

        # Tous les commentaires liés à cet article
        commentaires = article.commentaires.select_related("auteur").all()

        # Formulaire de commentaire
        formulaire_commentaire = CommentaireForm()

        # Articles pour la sidebar 
        autres_articles = (
            Article.objects
            .exclude(pk=article.pk)
            .select_related("categorie")
            .order_by("-date_creation")[:5]
        )

        # Injection dans le template
        context["commentaires"] = commentaires
        context["form"] = formulaire_commentaire
        context["articles_sidebar"] = autres_articles

        return context
    
    def post(self, request, *args, **kwargs):
            """
            Gère l'envoi d'un commentaire.
            """
            if not request.user.is_authenticated:
                messages.error(request, "Vous devez être connecté pour commenter.")
                return redirect("login")

            article = self.get_object()
            formulaire = CommentaireForm(request.POST)

            if formulaire.is_valid():
                nouveau_commentaire = formulaire.save(commit=False)
                nouveau_commentaire.article = article
                nouveau_commentaire.auteur = request.user
                nouveau_commentaire.save()

                messages.success(request, "Commentaire publié avec succès !")
            else:
                messages.error(request, "Erreur lors de l'envoi du commentaire.")

            return redirect("article_detail", pk=article.pk)

    