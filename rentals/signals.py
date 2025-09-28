import os

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Owner
from .models.leases import LeaseContract


@receiver(post_save, sender=LeaseContract)
def update_real_estate_unit_availability_on_lease_save(sender, instance, created, **kwargs):
    """
    Met à jour la disponibilité d'un bien quand un bail est créé ou modifié.
    """
    if instance.status == 'active':
        instance.real_estate_unit.is_available = False
        instance.real_estate_unit.save()
    else:
        # Si le bail est terminé/annulé, remettre le bien en disponibilité
        active_leases = LeaseContract.objects.filter(
            real_estate_unit=instance.real_estate_unit,
            status='active'
        ).exclude(pk=instance.pk)  # Exclut le bail courant

        if not active_leases.exists():
            instance.real_estate_unit.is_available = True
            instance.real_estate_unit.save()


@receiver(post_delete, sender=LeaseContract)
def update_real_estate_unit_availability_on_lease_delete(sender, instance, **kwargs):
    """
    Remet un bien en disponibilité quand son bail est supprimé.
    """
    active_leases = LeaseContract.objects.filter(
        real_estate_unit=instance.real_estate_unit,
        status='active'
    )
    if not active_leases.exists():
        instance.real_estate_unit.is_available = True
        instance.real_estate_unit.save()


@receiver(pre_save, sender=LeaseContract)
def validate_lease_dates(sender, instance, **kwargs):
    """
    Valide que les dates de bail ne chevauchent pas d'autres baux actifs pour le même bien.
    """
    if instance.pk:  # Si c'est une mise à jour (pas une création)
        return

    overlapping_leases = LeaseContract.objects.filter(
        real_estate_unit=instance.real_estate_unit,
        status='active'
    ).exclude(pk=instance.pk)  # Exclut le bail courant

    for lease in overlapping_leases:
        if (
            (instance.start_date <= lease.end_date and instance.end_date >= lease.start_date)
            if lease.end_date and instance.end_date
            else True  # Si une des dates est None, considère qu'il y a chevauchement
        ):
            raise ValueError(
                f"Un bail actif existe déjà pour ce bien du {lease.start_date} au {lease.end_date or '?'}. "
                "Veuillez choisir d'autres dates."
            )


@receiver(post_save, sender=LeaseContract)
def send_lease_confirmation_email(sender, instance, created, **kwargs):
    """
    Envoie un email de confirmation au locataire quand un bail est créé.
    """
    if created and instance.status == 'active':
        subject = f"Confirmation de votre bail - {instance.real_estate_unit}"
        message = (
            f"Bonjour {instance.tenant.first_name},\n\n"
            f"Votre bail pour le bien {instance.real_estate_unit} a été créé avec succès.\n"
            f"Date de début: {instance.start_date}\n"
            f"Loyer mensuel: {instance.real_estate_unit.monthly_rent} €\n"
            f"Merci de bien vouloir signer le contrat joint.\n\n"
            f"Cordialement,\nL'équipe de gestion"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.tenant.email],
            fail_silently=False,
        )


@receiver(post_save, sender=Owner)
def create_owner_directory(sender, instance, created, **kwargs):
    if created:
        # Crée un dossier pour stocker les documents du propriétaire
        owner_dir = os.path.join(settings.MEDIA_ROOT, 'owners', f'owner_{instance.id}')
        os.makedirs(owner_dir, exist_ok=True)
