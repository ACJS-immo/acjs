from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils import timezone

class LeaseType(models.TextChoices):
    STANDARD = 'standard', 'Standard Lease'
    COLOCATION = 'colocation', 'Colocation (Shared Accommodation)'

class LeaseContract(models.Model):
    property = models.ForeignKey(
        'Property',  # Référence circulaire résolue via string
        on_delete=models.CASCADE,
        related_name='lease_contracts'
    )
    tenant = models.ForeignKey(
        'Tenant',  # Référence circulaire
        on_delete=models.CASCADE,
        related_name='lease_contracts'
    )
    lease_type = models.CharField(
        max_length=20,
        choices=LeaseType.choices,
        default=LeaseType.STANDARD
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    has_solidarity_clause = models.BooleanField(
        default=False,
        help_text="For colocations: if True, all tenants are jointly liable."
    )
    flat_rate_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Fixed monthly charges (used when individual consumption cannot be measured)."
    )
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Security deposit amount."
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('terminated', 'Terminated'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft'
    )
    contract_document = models.FileField(
        upload_to='lease_contracts/',
        blank=True,
        help_text="Signed contract document (PDF)."
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Lease Contract"
        verbose_name_plural = "Lease Contracts"
        ordering = ['-start_date']

    def __str__(self):
        return f"Lease {self.id} - {self.property} ({self.tenant})"

    def get_absolute_url(self):
        return reverse('leases:detail', args=[str(self.id)])

    def total_monthly_amount(self):
        """Calculates total monthly amount based on lease type."""
        if self.lease_type == LeaseType.COLOCATION and self.flat_rate_charges > 0:
            return self.property.monthly_rent + self.flat_rate_charges
        return self.property.total_monthly_cost()

    def is_active(self):
        """Checks if the lease is currently active."""
        today = timezone.now().date()
        return self.status == 'active' and self.start_date <= today and (not self.end_date or self.end_date >= today)
