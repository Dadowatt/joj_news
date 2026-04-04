from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import Inscription, Connexion

def index(request):
    return render(request, 'index.html')


class Inscription(CreateView):
    form_class = Inscription
    success_url = reverse_lazy('connexion')
    template_name = 'registration/inscription.html'

class Connexion(LoginView):
    form_class = Connexion
    template_name = 'registration/connexion.html'