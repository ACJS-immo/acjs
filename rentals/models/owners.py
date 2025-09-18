from django.db import models
from django.core.validators import EmailValidator
from django.urls import reverse

class Owner(models.Model):
    """Represents a property owner (can own multiple properties)."""
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
