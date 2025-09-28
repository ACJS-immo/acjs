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


@pytest.mark.django_db
class TestBuildingModelExtra:
    """Tests additionnels pour améliorer la couverture du modèle Building."""

    def test_defaults_and_nullable_owner(self):
        """Vérifie les valeurs par défaut et que owner peut être null."""
        b = Building.objects.create(name="Sans Proprio", address="7 rue X")
        assert b.owner is None
        from decimal import Decimal
        assert b.total_general_charges == Decimal('0.00')
        assert b.has_individual_meters is True

    def test_available_real_estate_units_property(self):
        """Vérifie que available_real_estate_units ne retourne que les unités disponibles."""
        owner = Owner.objects.create(first_name="Ana", last_name="Pop", email="ana@example.com")
        b = Building.objects.create(name="Bloc B", address="2 ave B", owner=owner)
        u1 = RealEstateUnit.objects.create(
            building=b, unit_type='apartment', unit_number='B1', size_m2=40, monthly_rent=600, is_available=True
        )
        RealEstateUnit.objects.create(
            building=b, unit_type='apartment', unit_number='B2', size_m2=42, monthly_rent=620, is_available=False
        )
        available = list(b.available_real_estate_units)
        assert len(available) == 1
        assert available[0].id == u1.id

    def test_counts_with_prefetched_units_used(self):
        """Quand prefetched_real_estate_units est présent, les compteurs s'appuient dessus."""
        owner = Owner.objects.create(first_name="Luc", last_name="Martin", email="luc@example.com")
        b = Building.objects.create(name="Cité C", address="3 rue C", owner=owner)
        RealEstateUnit.objects.create(building=b, unit_type='apartment', unit_number='C1', size_m2=35, monthly_rent=500, is_available=True)
        RealEstateUnit.objects.create(building=b, unit_type='apartment', unit_number='C2', size_m2=36, monthly_rent=510, is_available=True)
        RealEstateUnit.objects.create(building=b, unit_type='apartment', unit_number='C3', size_m2=37, monthly_rent=520, is_available=False)
        # Simule une prélecture manuelle
        b.prefetched_real_estate_units = list(b.real_estate_units.all())
        assert b.total_real_estate_units_count == 3
        assert b.available_real_estate_units_count == 2
        assert b.rented_real_estate_units_count == 1
        # Et la propriété retourne la bonne liste
        available = b.available_real_estate_units
        assert isinstance(available, list)
        assert len(available) == 2

    def test_related_name_real_estate_units(self):
        owner = Owner.objects.create(first_name="Iris", last_name="Noel", email="iris@example.com")
        b = Building.objects.create(name="Tour D", address="4 allée D", owner=owner)
        assert b.real_estate_units.count() == 0
        RealEstateUnit.objects.create(building=b, unit_type='apartment', unit_number='D1', size_m2=55, monthly_rent=700, is_available=True)
        RealEstateUnit.objects.create(building=b, unit_type='apartment', unit_number='D2', size_m2=45, monthly_rent=650, is_available=True)
        assert b.real_estate_units.count() == 2

    def test_meta_ordering_by_name(self):
        Building.objects.create(name="Zeta", address="z")
        Building.objects.create(name="Alpha", address="a")
        Building.objects.create(name="Beta", address="b")
        names = [b.name for b in Building.objects.all()]
        assert names == sorted(names)