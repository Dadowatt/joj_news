from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView,ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import Inscription, Connexion
from .models import Article, Commentaire
from .forms import CommentaireForm
from django.db.models import Q


class Inscription(CreateView):
    form_class = Inscription
    success_url = reverse_lazy('connexion')
    template_name = 'registration/inscription.html'

class Connexion(LoginView):
    form_class = Connexion
    template_name = 'registration/connexion.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

def index(request):
    # Récupérer tous les articles avec les relations nécessaires
    articles = Article.objects.select_related("categorie", "auteur").all().order_by('-date_creation')

    # Carrousel des 4 premiers articles
    hero_articles = articles[:4]

    # Grille principale pour les articles suivants
    grid_articles = articles[4:9]

    # Commentaires récents : les 5 derniers commentaires
    commentaires = Commentaire.objects.select_related("auteur", "article").order_by('-date_creation')[:5]

    context = {
        'articles': articles,           
        'hero_articles': hero_articles, 
        'grid_articles': grid_articles, 
        'commentaires': commentaires,   
    }
    return render(request, 'index.html', context)

class ArticleListView(ListView):
    model = Article
    template_name = "index.html"
    context_object_name = "articles"
    paginate_by = 4  
    
    def get_queryset(self):
        queryset = Article.objects.select_related("categorie", "auteur").all().order_by("-date_creation")

        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(categorie__nom__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = self.get_queryset()

        context["query"] = self.request.GET.get("q")

        context["hero_articles"] = articles[:4]
        context["grid_articles"] = articles[5:9] if articles.count() > 4 else articles[:4]

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
        form = CommentaireForm()
        if self.request.GET.get("comment_posted") == "1":
            form.fields["contenu"].widget.attrs["placeholder"] = ""
        context["form"] = form

        # Articles pour le sidebar
        context["articles_sidebar"] = Article.objects.exclude(pk=article.pk).order_by("-date_creation")[:5]
        return context

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = article
            commentaire.auteur = request.user
            commentaire.save()
            return redirect(f"/article/{article.pk}/?comment_posted=1")
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