from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Commentaire


@receiver(post_save, sender=Commentaire)
def envoyer_email_commentaire(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject="Nouveau commentaire ajouté",
            message=f"""
Un nouveau commentaire a été publié !

 Article : {instance.article.titre}
 Auteur : {instance.auteur.username}

 Message :
{instance.contenu}
""",
            from_email="noreply@joj.com",
            recipient_list=["admin@joj.com"],
            fail_silently=True,
        )