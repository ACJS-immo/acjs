from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class PropertyType(models.TextChoices):
    APARTMENT = 'apartment', _("Apartment")
    HOUSE = 'house', _("House")
    ROOM = 'room', _("Room (for shared accommodation)")

class Property(models.Model):
    building = models.ForeignKey(
        'Building', on_delete=models.CASCADE,
        related_name='properties', verbose_name=_("Building")
    )
    owner = models.ForeignKey(
        'Owner', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='properties', verbose_name=_("Owner")
    )
    property_type = models.CharField(
        max_length=20, choices=PropertyType.choices,
        verbose_name=_("Property Type")
    )
    unit_number = models.CharField(
        max_length=50, verbose_name=_("Unit Number"),
        help_text=_("Apartment number, room number, or other identifier.")
    )
    size_m2 = models.DecimalField(
        max_digits=6, decimal_places=2,
        verbose_name=_("Size (m²)"), validators=[MinValueValidator(0)]
    )
    monthly_rent = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name=_("Monthly Rent"), validators=[MinValueValidator(0)]
    )
    specific_charges = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name=_("Specific Charges"), validators=[MinValueValidator(0)]
    )
    is_available = models.BooleanField(default=True, verbose_name=_("Available"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
        ordering = ['building__name', 'unit_number']

    def __str__(self):
        return f"{self.get_property_type_display()} {self.unit_number} ({self.building.name})"

    @property
    def total_monthly_cost(self):
        """Retourne le coût mensuel total (loyer + charges spécifiques)."""
        return self.monthly_rent + self.specific_charges

    @property
    def current_owner(self):
        """Retourne le propriétaire effectif (propriétaire de la propriété ou de l'immeuble)."""
        return self.owner if self.owner else self.building.owner

    @property
    def active_lease(self):
        """Retourne le bail actif pour cette propriété (ou None)."""
        return self.lease_contracts.filter(status='active').first()

    @property
    def has_active_lease(self):
        """Retourne True si cette propriété a un bail actif."""
        return self.lease_contracts.filter(status='active').exists()

    @property
    def lease_history(self):
        """Retourne l'historique des baux pour cette propriété."""
        return self.lease_contracts.all().order_by('-start_date')

    def get_absolute_url(self):
        return reverse('rentals:properties_detail', args=[str(self.id)])
