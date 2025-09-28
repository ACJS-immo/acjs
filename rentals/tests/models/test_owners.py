import pytest
from django.urls import reverse

from rentals.models import Owner, Building, RealEstateUnit


@pytest.mark.django_db
class TestOwnerModel:
    def test_owner_creation_and_str(self):
        owner = Owner.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com")
        assert owner.first_name == "John"
        assert owner.last_name == "Doe"
        assert owner.email == "john.doe@example.com"
        # __str__ should be "Last First"
        assert str(owner) == "Doe John"
        # full_name should be "First Last"
        assert owner.full_name == "John Doe"

    def test_buildings_count(self, owner):
        # Initially no buildings
        assert owner.buildings_count == 0
        # Create one building
        Building.objects.create(name="Immeuble A", address="1 rue A", owner=owner)
        assert owner.buildings_count == 1
        # Create another building
        Building.objects.create(name="Immeuble B", address="2 rue B", owner=owner)
        assert owner.buildings_count == 2

    def test_properties_count_and_total_revenue(self, owner):
        # Needs a building to attach units
        building = Building.objects.create(name="Résidence Parc", address="10 avenue du Parc", owner=owner)
        assert owner.properties_count == 0
        assert owner.total_revenue == 0

        # Create two units owned directly by this owner
        RealEstateUnit.objects.create(
            building=building,
            owner=owner,
            unit_type='apartment',
            unit_number='A1',
            size_m2=45.0,
            monthly_rent=750.0,
            is_available=True,
        )
        RealEstateUnit.objects.create(
            building=building,
            owner=owner,
            unit_type='apartment',
            unit_number='A2',
            size_m2=50.0,
            monthly_rent=800.0,
            is_available=False,
        )

        assert owner.properties_count == 2
        # total_revenue sums monthly_rent of all units linked to owner
        from decimal import Decimal
        assert owner.total_revenue == Decimal('1550.00')

    def test_get_absolute_url(self, owner):
        expected = reverse('rentals:owners_detail', args=[owner.pk])
        assert owner.get_absolute_url() == expected
