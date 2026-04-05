from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
     path('', views.index, name="index"),
     path('inscription/', views.Inscription.as_view(), name='inscription'),
     path('connexion/', views.Connexion.as_view(), name='connexion'),
     path("",            views.ArticleListView.as_view(),  name="home"),
     path("article/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
     path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
