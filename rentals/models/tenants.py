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
