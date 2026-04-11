# JOJ News - Journal Officiel des Supporters

Application web Django permettant la gestion d’articles officiels et l’interaction des utilisateurs via des commentaires, avec notifications automatiques par email.

## Stack technique

- Django==6.0.3
- Bootstrap 5
- MySQL
- Django Auth
- Signals (post_save)
- Class-Based Views (CBV)
- django-cleanup==9.0.0
- mysqlclient==2.2.8
- pillow==12.2.0
- python-dotenv==1.2.2
- asgiref==3.11.1
- sqlparse==0.5.5

---

## Fonctionnalités

### Administration
- Création, modification et suppression des catégories (ex : Athlétisme, Natation, etc.)
- Gestion complète des articles
- Accès réservé aux utilisateurs avec is_staff=True

### Utilisateurs
- Inscription et connexion avec Django Auth
- Consultation des articles publiés
- Interaction via commentaires

### Commentaires
- Ajout de commentaires uniquement pour les utilisateurs connectés
- Modification et suppression uniquement de ses propres commentaires
- Sécurisation des accès via UserPassesTestMixin
- Affichage des commentaires sous chaque article

### Notifications
- Déclenchement automatique d’un email lors de la création d’un commentaire
- Utilisation du signal post_save
- Email envoyé à l’administrateur (visible dans la console en développement)

---

## Sécurité

- Accès /admin strictement réservé aux staff
- Vérification des permissions pour modification et suppression des commentaires
- Empêchement de toute modification via URL non autorisée
- Séparation claire entre utilisateurs et administrateurs

---

## Interface utilisateur

- Interface responsive avec Bootstrap 5
- Design propre et cohérent
- Mise en page adaptée mobile et desktop
- Affichage clair des articles et commentaires

---

## Organisation du projet (Git)

- Une branche main contenant la version stable finale
- Travail en binôme collaboratif
- Fusion finale des branches dans main après validation

---

## Installation du projet

```bash
git clone <url-du-repo>
cd joj-news

python -m venv venv

# activation environnement virtuel
# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver