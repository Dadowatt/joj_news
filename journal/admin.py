from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Categorie, Article, Commentaire, Utilisateur

# @admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    model = Utilisateur
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('-date_joined','username')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name')
        }),

        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),

        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    ordering = ('nom',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ('titre', 'categorie', 'auteur', 'date_creation', 'date_modification')
    list_filter = ('categorie', 'date_creation', 'auteur')
    search_fields = ('titre', 'contenu', 'resume')

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

    readonly_fields = ('date_creation', 'date_modification')

    def save_model(self, request, obj, form, change):
        if not obj.auteur:
            obj.auteur = request.user
        super().save_model(request, obj, form, change)


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'article', 'date_creation', 'contenu_court')
    list_filter = ('date_creation', 'article')
    search_fields = ('contenu', 'auteur__email', 'article__titre')
    ordering = ('-date_creation',)
    def contenu_court(self, obj):
        return obj.contenu[:50] + "..." if len(obj.contenu) > 50 else obj.contenu
    contenu_court.short_description = "Commentaire"

