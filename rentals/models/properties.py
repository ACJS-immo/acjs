from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from .buildings import Building
from .owners import Owner

class PropertyType(models.TextChoices):
    APARTMENT = 'apartment', 'Apartment'
    HOUSE = 'house', 'House'
    ROOM = 'room', 'Room (for shared accommodation)'

class Property(models.Model):
    """Represents a rentable unit (apartment, house, or individual room)."""
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='properties'
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties',
        help_text="Owner of this specific property (defaults to building owner)."
    )
    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices
    )
    unit_number = models.CharField(
        max_length=50,
        help_text="Apartment number, room number, or other identifier."
    )
    size_m2 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    monthly_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    specific_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Monthly charges specific to this unit (e.g., individual water meter)."
    )
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ['building__name', 'unit_number']

    def __str__(self):
        return f"{self.get_property_type_display()} {self.unit_number} ({self.building.name})"

    def get_absolute_url(self):
        return reverse('rentals:properties_detail', args=[str(self.id)])

    def total_monthly_cost(self):
        """Returns total monthly cost (rent + specific charges)."""
        return self.monthly_rent + self.specific_charges

    def current_owner(self):
        """Returns the effective owner (property owner or building owner)."""
        return self.owner if self.owner else self.building.owner

    @property
    def active_leases(self):
        """Retourne une liste des baux actifs pour cette propriété.

           Utilise les données préchargées si disponibles (via prefetch_related),
           sinon effectue une requête en base de données.

           Returns:
               QuerySet: Liste des baux actifs.
           """
        if hasattr(self, 'prefetched_leases'):  # Si les données sont préchargées
            return [lease for lease in self.prefetched_leases if lease.status == 'active']
        return self.lease_contracts.filter(status='active')

    @property
    def has_active_lease(self):
        """Retourne True si cette propriété a un bail actif."""
        if hasattr(self, 'prefetched_leases'):
            return any(lease.status == 'active' for lease in self.prefetched_leases)
        return self.lease_contracts.filter(status='active').exists()