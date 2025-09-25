from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class LeaseType(models.TextChoices):
    STANDARD = 'standard', _("Standard Lease")
    COLOCATION = 'colocation', _("Colocation (Shared Accommodation)")

class LeaseContract(models.Model):
    property = models.ForeignKey(
        'Property', on_delete=models.CASCADE,
        related_name='lease_contracts', verbose_name=_("Property")
    )
    tenant = models.ForeignKey(
        'Tenant', on_delete=models.CASCADE,
        related_name='lease_contracts', verbose_name=_("Tenant")
    )
    lease_type = models.CharField(
        max_length=20, choices=LeaseType.choices,
        default=LeaseType.STANDARD, verbose_name=_("Lease Type")
    )
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("End Date"))
    has_solidarity_clause = models.BooleanField(
        default=False, verbose_name=_("Solidarity Clause"),
        help_text=_("For colocations: if True, all tenants are jointly liable.")
    )
    flat_rate_charges = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name=_("Flat Rate Charges"),
        help_text=_("Fixed monthly charges (used when individual consumption cannot be measured).")
    )
    deposit_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name=_("Deposit Amount"),
        help_text=_("Security deposit amount.")
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', _("Draft")),
            ('active', _("Active")),
            ('terminated', _("Terminated")),
            ('cancelled', _("Cancelled")),
        ],
        default='draft', verbose_name=_("Status")
    )
    contract_document = models.FileField(
        upload_to='lease_contracts/', blank=True,
        verbose_name=_("Contract Document"),
        help_text=_("Signed contract document (PDF).")
    )
    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    class Meta:
        verbose_name = _("Lease Contract")
        verbose_name_plural = _("Lease Contracts")
        ordering = ['-start_date']

    def __str__(self):
        return f"Lease {self.id} - {self.property} ({self.tenant})"

    @property
    def total_monthly_amount(self):
        """Calcule le montant mensuel total en fonction du type de bail."""
        if self.lease_type == LeaseType.COLOCATION and self.flat_rate_charges > 0:
            return self.property.monthly_rent + self.flat_rate_charges
        return self.property.total_monthly_cost

    @property
    def is_active(self):
        """Vérifie si le bail est actuellement actif."""
        today = timezone.now().date()
        return self.status == 'active' and self.start_date <= today and (not self.end_date or self.end_date >= today)

    @property
    def duration_in_months(self):
        """Retourne la durée du bail en mois."""
        if not self.end_date:
            return None
        delta = self.end_date - self.start_date
        return delta.days // 30  # Approximation

    @property
    def remaining_days(self):
        """Retourne le nombre de jours restants avant la fin du bail."""
        if not self.end_date or not self.is_active:
            return None
        return (self.end_date - timezone.now().date()).days


    def get_absolute_url(self):
        return reverse('leases:detail', args=[str(self.id)])