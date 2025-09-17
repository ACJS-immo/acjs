from django.db import models

class RealEstateProperty(models.Model):
    displayed_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Displayed Price")
    surface_area = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Surface Area (m²)")
    property_tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Property Tax")

    purchase_date = models.DateField(verbose_name="Purchase Date")
    rental_start_date = models.DateField(verbose_name="Rental Start Date")

    deferral_period = models.IntegerField(default=0, verbose_name="Deferral Period (months)")
    first_year_rental_months = models.IntegerField(verbose_name="Rental Months in 1st Year")

    price_per_square_meter = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Price per m²")
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Monthly Rent")
    rent_per_square_meter = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Rent per m²")

    def __str__(self):
        return f"Property: {self.displayed_price}€, {self.surface_area}m²"

    class Meta:
        verbose_name = "Real Estate Property"
        verbose_name_plural = "Real Estate Properties"
