from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Commentaire
from django.core.mail import send_mail


@receiver(post_save, sender=Commentaire)
def envoyer_email_commentaire(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject="Nouveau commentaire",
            message=f"Un nouveau commentaire a été ajouté sur l'article : {instance.article.titre}",
            from_email="noreply@joj.com",
            recipient_list=["admin@joj.com"],
            fail_silently=True,
        )