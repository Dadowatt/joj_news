from django.urls import path
from . import views

urlpatterns = [
     path('inscription/', views.Inscription.as_view(), name='inscription'),
     path('connexion/', views.Connexion.as_view(), name='connexion'),

]