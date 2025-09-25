from django.db import models
from django.core.validators import EmailValidator
from django.urls import reverse

class Tenant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Invalid email format.")]
    )
    phone = models.CharField(max_length=20, blank=True)
    id_document = models.FileField(
        upload_to='tenants/id_documents/',
        blank=True,
        help_text="Scan of ID or passport."
    )
    emergency_contact = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name and phone of emergency contact."
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse('tenants:detail', args=[str(self.id)])

    @property
    def active_leases(self):
        """Retourne les baux actifs pour ce locataire (optimisé pour prefetch_related)."""
        if hasattr(self, 'prefetched_leases'):  # Si les données sont préchargées
            return [lease for lease in self.prefetched_leases if lease.status == 'active']
        return self.lease_contracts.filter(status='active')

    @property
    def has_active_lease(self):
        """Retourne True si ce locataire a un bail actif."""
        if hasattr(self, 'prefetched_leases'):
            return any(lease.status == 'active' for lease in self.prefetched_leases)
        return self.lease_contracts.filter(status='active').exists()

    @property
    def total_leases_count(self):
        """Retourne le nombre total de baux pour ce locataire."""
        if hasattr(self, 'prefetched_leases'):
            return len(self.prefetched_leases)
        return self.lease_contracts.count()

    @property
    def active_leases_count(self):
        """Retourne le nombre de baux actifs pour ce locataire."""
        if hasattr(self, 'prefetched_leases'):
            return len([lease for lease in self.prefetched_leases if lease.status == 'active'])
        return self.lease_contracts.filter(status='active').count()