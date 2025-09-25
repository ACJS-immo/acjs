import pytest
from django.db import models

from rentals.models import Building, Owner, RealEstateUnit


@pytest.mark.django_db
class TestBuildingModel:
    """Tests unitaires pour le modèle Building."""

    def test_building_creation(self):
        """Test la création d'un immeuble."""
        owner = Owner.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        building = Building.objects.create(
            name="Building A",
            address="123 Main St",
            total_general_charges=300.0,
            has_individual_meters=True,
            owner=owner
            )
        assert building.name == "Building A"
        assert building.address == "123 Main St"
        assert building.total_general_charges == 300.0
        assert building.has_individual_meters is True
        assert building.owner == owner

    def test_building_str_method(self):
        """Test la méthode __str__ du modèle Building."""
        owner = Owner.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        building = Building.objects.create(
            name="Building A",
            address="123 Main St",
            owner=owner
            )
        assert str(building) == "Building A (123 Main St)"

    def test_available_properties_count_with_no_properties(self):
        """Test available_properties_count quand il n'y a pas de propriétés."""
        owner = Owner.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        building = Building.objects.create(
            name="Building A",
            address="123 Main St",
            owner=owner
            )
        assert building.available_real_estate_units_count == 0
        assert building.total_real_estate_units_count == 0
        assert building.rented_real_estate_units_count == 0

    def test_available_properties_count_with_properties(self):
        """Test available_properties_count avec des propriétés."""
        owner = Owner.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        building = Building.objects.create(
            name="Building A",
            address="123 Main St",
            owner=owner
            )

        # Ajoute des propriétés
        RealEstateUnit.objects.create(
            building=building,
            unit_type='apartment',
            unit_number="A1",
            size_m2=50.0,
            monthly_rent=800.0,
            is_available=True  # Disponible
            )
        RealEstateUnit.objects.create(
            building=building,
            unit_type='apartment',
            unit_number="A2",
            size_m2=60.0,
            monthly_rent=900.0,
            is_available=False  # Louée
            )

        assert building.available_real_estate_units_count == 1
        assert building.total_real_estate_units_count == 2
        assert building.rented_real_estate_units_count == 1

    def test_building_get_absolute_url(self):
        """Test la méthode get_absolute_url."""
        owner = Owner.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        building = Building.objects.create(
            name="Building A",
            address="123 Main St",
            owner=owner
            )
        from django.urls import reverse
        assert building.get_absolute_url() == reverse('rentals:buildings_detail', args=[building.pk])

    def test_building_with_annotations(self):
        """Test les annotations sur les immeubles."""
        owner = Owner.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        building = Building.objects.create(
            name="Building A",
            address="123 Main St",
            owner=owner
            )

        # Ajoute des propriétés
        RealEstateUnit.objects.create(
            building=building,
            unit_type='apartment',
            unit_number="A1",
            size_m2=50.0,
            monthly_rent=800.0,
            is_available=True
            )
        RealEstateUnit.objects.create(
            building=building,
            unit_type='apartment',
            unit_number="A2",
            size_m2=60.0,
            monthly_rent=900.0,
            is_available=False
            )

        # Utilise annotate dans une requête
        from django.db.models import Count
        buildings = Building.objects.annotate(
            available_count=Count('real_estate_units', filter=models.Q(real_estate_units__is_available=True)),
            total_count=Count('real_estate_units'),
            rented_count=Count('real_estate_units', filter=models.Q(real_estate_units__is_available=False))
            )
        annotated_building = buildings.get(pk=building.pk)
        assert annotated_building.available_real_estate_units_count == 1
        assert annotated_building.total_real_estate_units_count == 2
        assert annotated_building.rented_real_estate_units_count == 1
