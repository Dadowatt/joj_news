from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('inscription/', views.Inscription.as_view(), name='inscription'),
    path('connexion/', views.Connexion.as_view(), name='connexion'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path("commentaire/<int:pk>/edit/", views.CommentaireUpdateView.as_view(), name="comment_edit"),
    path("commentaire/<int:pk>/delete/", views.CommentaireDeleteView.as_view(), name="comment_delete"),
]
