from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Categorie, Article
from .models import Utilisateur

from django.contrib import admin
from .models import Categorie, Article, Commentaire


# CATEGORIE ADMIN

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    ordering = ('nom',)


#  ARTICLE ADMIN

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    #  LISTE
    list_display = ('titre', 'categorie', 'auteur', 'date_creation', 'date_modification')
    
    #  FILTRES
    list_filter = ('categorie', 'date_creation', 'auteur')
    
    #  RECHERCHE
    search_fields = ('titre', 'contenu', 'resume')
    
  

    #  ORGANISATION FORMULAIRE
    fieldsets = (
        ('Contenu principal', {
            'fields': ('titre', 'categorie', 'auteur')
        }),
        ('Contenu éditorial', {
            'fields': ('resume', 'contenu')
        }),
        ('Média', {
            'fields': ('image',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
        }),
    )

    #  CHAMPS READONLY
    readonly_fields = ('date_creation', 'date_modification')

    #  AUTO ATTRIBUTION AUTEUR 
    def save_model(self, request, obj, form, change):
        if not obj.auteur:
            obj.auteur = request.user
        super().save_model(request, obj, form, change)


# COMMENTAIRE ADMIN

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):

    #  LISTE
    list_display = ('auteur', 'article', 'date_creation', 'contenu_court')

    #  FILTRES
    list_filter = ('date_creation', 'article')

    #  RECHERCHE
    search_fields = ('contenu', 'auteur__email', 'article__titre')

    #  ORDER
    ordering = ('-date_creation',)

    #  PREVIEW CONTENU
    def contenu_court(self, obj):
        return obj.contenu[:50] + "..." if len(obj.contenu) > 50 else obj.contenu
    contenu_court.short_description = "Commentaire"

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    
    #  AFFICHAGE LISTE
    list_display = ('email', 'username', 'is_staff', 'is_active', 'date_joined')
    
    #  FILTRES
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    
    #  RECHERCHE
    search_fields = ('email', 'username')
    
    #  ORDRE
    ordering = ('-date_joined',)

    #  CHAMPS DÉTAILLÉS
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        
        ('Informations personnelles', {
            'fields': ('username', 'first_name', 'last_name')
        }),

        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),

        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    #  FORMULAIRE CRÉATION USER
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )