from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Building(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    address = models.TextField(verbose_name=_("Address"))
    total_general_charges = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name=_("Total General Charges")
        )
    has_individual_meters = models.BooleanField(
        default=True,
        verbose_name=_("Individual Meters"),
        help_text=_("Can individual consumption (water, electricity) be measured per unit?")
        )
    owner = models.ForeignKey(
        'Owner', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='buildings', verbose_name=_("Owner")
        )


    class Meta:
        verbose_name = _("Building")
        verbose_name_plural = _("Buildings")
        ordering = ['name']


    def __str__(self):
        return f"{self.name} ({self.address})"

    @property
    def available_real_estate_units(self):  # ✅ Renommé
        """Retourne les unités disponibles dans cet immeuble."""
        if hasattr(self, 'prefetched_real_estate_units'):  # ✅ Renommé
            return [unit for unit in self.prefetched_real_estate_units if unit.is_available]
        return self.real_estate_units.filter(is_available=True)  # ✅ Renommé

    @property
    def available_real_estate_units_count(self):  # ✅ Renommé
        """Retourne le nombre d'unités disponibles."""
        if hasattr(self, 'prefetched_real_estate_units'):
            return len([unit for unit in self.prefetched_real_estate_units if unit.is_available])
        return self.real_estate_units.filter(is_available=True).count()  # ✅ Renommé

    @property
    def rented_real_estate_units_count(self):  # ✅ Renommé
        """Retourne le nombre d'unités louées."""
        if hasattr(self, 'prefetched_real_estate_units'):
            return len([unit for unit in self.prefetched_real_estate_units if not unit.is_available])
        return self.real_estate_units.filter(is_available=False).count()  # ✅ Renommé

    @property
    def total_real_estate_units_count(self):  # ✅ Renommé
        """Retourne le nombre total d'unités."""
        if hasattr(self, 'prefetched_real_estate_units'):
            return len(self.prefetched_real_estate_units)
        return self.real_estate_units.count()  # ✅ Renommé

    def get_absolute_url(self):
        return reverse('rentals:buildings_detail', args=[str(self.id)])


class ChargeDistribution(models.Model):
    """Tracks how general building charges are distributed among real_estate_units."""
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='charge_distributions'
        )
    real_estate_unit = models.ForeignKey(
        'RealEstateUnit',  # Référence circulaire résolue via string
        on_delete=models.CASCADE,
        related_name='charge_distributions'
        )
    distribution_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of general charges allocated to this property (0-100)."
        )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)


    class Meta:
        verbose_name = "Charge Distribution"
        verbose_name_plural = "Charge Distributions"
        unique_together = [['building', 'real_estate_unit', 'start_date']]


    def __str__(self):
        return f"{self.real_estate_unit} - {self.distribution_percentage}% of {self.building.name}'s charges"
