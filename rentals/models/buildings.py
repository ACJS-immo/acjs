from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone
from .owners import Owner

class Building(models.Model):
    """Represents a physical building containing rentable properties."""
    name = models.CharField(max_length=200)
    address = models.TextField()
    total_general_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total monthly general charges for the entire building."
    )
    has_individual_meters = models.BooleanField(
        default=True,
        help_text="Can individual consumption (water, electricity) be measured per unit?"
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='buildings',
        help_text="Main owner of the building (can be overridden per property)."
    )

    class Meta:
        verbose_name = "Building"
        verbose_name_plural = "Buildings"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.address})"

    def get_absolute_url(self):
        return reverse('rentals:buildings_detail', args=[str(self.id)])

    @property
    def available_properties_count(self):
        """Retourne le nombre de propriétés disponibles dans cet immeuble."""
        return self.properties.filter(is_available=True).count()

    @property
    def total_properties_count(self):
        """Retourne le nombre total de propriétés dans cet immeuble."""
        return self.properties.count()

    @property
    def rented_properties_count(self):
        """Retourne le nombre de propriétés louées dans cet immeuble."""
        return self.properties.filter(is_available=False).count()

class ChargeDistribution(models.Model):
    """Tracks how general building charges are distributed among properties."""
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='charge_distributions'
    )
    property = models.ForeignKey(
        'Property',  # Référence circulaire résolue via string
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
        unique_together = [['building', 'property', 'start_date']]

    def __str__(self):
        return f"{self.property} - {self.distribution_percentage}% of {self.building.name}'s charges"
