from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Owner(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    address = models.TextField(blank=True, verbose_name=_("Address"))
    tax_number = models.CharField(max_length=50, blank=True, verbose_name=_("Tax Number"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    class Meta:
        verbose_name = _("Owner")
        verbose_name_plural = _("Owners")
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def full_name(self):
        """Retourne le nom complet du propriétaire."""
        return f"{self.first_name} {self.last_name}"

    @property
    def buildings_count(self):
        """Retourne le nombre d'immeubles possédés par ce propriétaire."""
        return self.buildings.count()

    @property
    def properties_count(self):
        """Retourne le nombre de propriétés possédées par ce propriétaire."""
        return self.properties.count()

    @property
    def total_revenue(self):
        """Retourne le revenu total généré par les propriétés de ce propriétaire."""
        return sum(property.monthly_rent for property in self.properties.all())


    def get_absolute_url(self):
        return reverse('rentals:owners_detail', args=[str(self.id)])
