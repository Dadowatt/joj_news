from django.shortcuts import redirect
from django.views.generic import CreateView,ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import Inscription, Connexion
from .models import Article, Commentaire
from .forms import CommentaireForm
from django.contrib import messages



class InscriptionView(CreateView):
    form_class = Inscription
    success_url = reverse_lazy('connexion')
    template_name = 'registration/inscription.html'

class ConnexionView(LoginView):
    form_class = Connexion
    template_name = 'registration/connexion.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')


class ArticleListView(ListView):
    model = Article
    template_name = "index.html"
    context_object_name = "articles"
    paginate_by = 9  

    def get_queryset(self):
        # récupère tous les articles avec relations pour éviter les requêtes multiples
        return Article.objects.select_related("categorie", "auteur").all().order_by("-date_creation")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = self.get_queryset()

        # articles pour le carrousel 
        context["hero_articles"] = articles[:4]

        # articles pour la grille principale 
        context["grid_articles"] = articles[4:9]

        # dernier articles pour la sidebar
        context["articles_sidebar"] = articles[1:6]

        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context["commentaires"] = article.commentaires.select_related("auteur").all()
        context["form"] = CommentaireForm()

        # Articles pour le sidebar
        context["articles_sidebar"] = Article.objects.exclude(pk=article.pk).order_by("-date_creation")[:5]
        return context
    
    def post(self, request, *args, **kwargs):
            """
            Gère l'envoi d'un commentaire.
            """
            if not request.user.is_authenticated:
                messages.error(request, "Vous devez être connecté pour commenter.")
                return redirect("login")

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = article
            commentaire.auteur = request.user
            commentaire.save()
            return redirect("article_detail", pk=article.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)

class CommentaireUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Commentaire
    form_class = CommentaireForm
    template_name = "commentaire_edit.html"

    def get_success_url(self):
        return self.object.article.get_absolute_url()

    def test_func(self):
        commentaire = self.get_object()
        return self.request.user == commentaire.auteur

class CommentaireDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Commentaire
    template_name = "commentaire_delete.html"

    def get_success_url(self):
        return self.object.article.get_absolute_url()

    def test_func(self):
        commentaire = self.get_object()
        return self.request.user == commentaire.auteur
