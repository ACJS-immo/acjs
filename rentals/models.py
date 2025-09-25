from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.utils import timezone
from django.urls import reverse

# ========== OWNER MODEL ==========
class Owner(models.Model):
    """Represents a property owner (can own multiple real_estate_units)."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Invalid email format.")]
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    tax_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Tax identification number (if applicable)."
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse('owners:detail', args=[str(self.id)])

# ========== BUILDING MODEL ==========
class Building(models.Model):
    """Represents a physical building containing rentable real_estate_units."""
    name = models.CharField(max_length=200)
    address = models.TextField()
    total_general_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total monthly general charges for the entire building (e.g., cleaning, maintenance)."
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
        return reverse('buildings:detail', args=[str(self.id)])

# ========== PROPERTY MODELS ==========
class PropertyType(models.TextChoices):
    APARTMENT = 'apartment', 'Apartment'
    HOUSE = 'house', 'House'
    ROOM = 'room', 'Room (for shared accommodation)'

class Property(models.Model):
    """Represents a rentable unit (apartment, house, or individual room)."""
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='real_estate_units'
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='real_estate_units',
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
        return reverse('real_estate_units:detail', args=[str(self.id)])

    def total_monthly_cost(self):
        """Returns total monthly cost (rent + specific charges)."""
        return self.monthly_rent + self.specific_charges

    def current_owner(self):
        """Returns the effective owner (property owner or building owner)."""
        return self.owner if self.owner else self.building.owner

# ========== TENANT MODEL ==========
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

# ========== LEASE MODELS ==========
class LeaseType(models.TextChoices):
    STANDARD = 'standard', 'Standard Lease'
    COLOCATION = 'colocation', 'Colocation (Shared Accommodation)'

class LeaseContract(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='lease_contracts'
    )
    tenant = models.ForeignKey(
        Tenant,
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

# ========== CHARGE DISTRIBUTION ==========
class ChargeDistribution(models.Model):
    """Tracks how general building charges are distributed among real_estate_units."""
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='charge_distributions'
    )
    property = models.ForeignKey(
        Property,
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
