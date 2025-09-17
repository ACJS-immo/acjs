from django import forms
from .models import RealEstateProperty

class RealEstatePropertyForm(forms.ModelForm):
    class Meta:
        model = RealEstateProperty
        fields = [
            'displayed_price', 'surface_area', 'property_tax',
            'purchase_date', 'rental_start_date',
            'deferral_period', 'first_year_rental_months',
            'price_per_square_meter', 'monthly_rent', 'rent_per_square_meter'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'rental_start_date': forms.DateInput(attrs={'type': 'date'}),
        }
