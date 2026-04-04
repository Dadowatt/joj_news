from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Categorie, Article, Utilisateur
from .models import Utilisateur



@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    model = Utilisateur
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(Categorie)
admin.site.register(Article)