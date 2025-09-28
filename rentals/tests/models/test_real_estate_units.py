from datetime import date, timedelta

import pytest

from rentals.models import RealEstateUnit, LeaseContract, Building, Owner


@pytest.mark.django_db
class TestRealEstateUnitModel:
    def test_real_estate_unit_creation_and_str(self, building):
        u = RealEstateUnit.objects.create(
            building=building,
            unit_type='apartment',
            unit_number="A1",
            size_m2=50.0,
            monthly_rent=800.0,
            is_available=True,
        )
        assert u.building == building
        assert u.unit_type == 'apartment'
        assert u.unit_number == "A1"
        # specific_charges par défaut = 0
        from decimal import Decimal
        assert u.specific_charges == Decimal('0.00')
        # __str__ utilise le libellé du type et le nom du building
        assert str(u) == f"Apartment A1 ({building.name})"

    def test_total_monthly_cost_property(self, real_estate_unit):
        # 800 (loyer) + 50 (charges) selon la fixture
        from decimal import Decimal
        assert real_estate_unit.total_monthly_cost == Decimal('850.00')

    def test_current_owner_fallback_and_override(self, owner):
        b = Building.objects.create(name="Bloc E", address="5 rue E", owner=owner)
        # Pas d'owner sur l'unité -> fallback sur l'owner du building
        u1 = RealEstateUnit.objects.create(
            building=b, unit_type='apartment', unit_number='E1', size_m2=40, monthly_rent=600
        )
        assert u1.owner is None
        assert u1.current_owner == owner
        # Owner explicite sur l'unité -> prioritaire
        other = Owner.objects.create(first_name="Mia", last_name="Lopez", email="mia@example.com")
        u2 = RealEstateUnit.objects.create(
            building=b, owner=other, unit_type='apartment', unit_number='E2', size_m2=41, monthly_rent=610
        )
        assert u2.current_owner == other

    def test_active_lease_and_has_active_lease_and_history(self, real_estate_unit, tenant):
        # Aucun bail actif au départ
        assert real_estate_unit.active_lease is None
        assert real_estate_unit.has_active_lease is False
        # Ajoute un bail terminé dans le passé
        LeaseContract.objects.create(
            real_estate_unit=real_estate_unit,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today() - timedelta(days=400),
            end_date=date.today() - timedelta(days=200),
            status='terminated'
        )
        assert real_estate_unit.active_lease is None
        assert real_estate_unit.has_active_lease is False
        # Ajoute un bail actif courant
        active = LeaseContract.objects.create(
            real_estate_unit=real_estate_unit,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() + timedelta(days=300),
            status='active'
        )
        # Propriétés d'accès
        assert real_estate_unit.has_active_lease is True
        assert real_estate_unit.active_lease.id == active.id
        # Historique trié décroissant par start_date
        history = list(real_estate_unit.lease_history)
        assert len(history) == 2
        assert history[0].start_date >= history[1].start_date

    def test_related_names_from_building_and_owner(self, owner):
        b = Building.objects.create(name="Immeuble X", address="x", owner=owner)
        assert b.real_estate_units.count() == 0
        u1 = RealEstateUnit.objects.create(building=b,
                                           unit_type='apartment',
                                           unit_number='X1',
                                           size_m2=30,
                                           monthly_rent=400
                                           )
        u2 = RealEstateUnit.objects.create(building=b,
                                           owner=owner,
                                           unit_type='apartment',
                                           unit_number='X2',
                                           size_m2=31,
                                           monthly_rent=410
                                           )
        assert b.real_estate_units.count() == 2
        # L'owner doit voir les unités liées via related_name
        assert owner.real_estate_units.count() == 1
        assert owner.real_estate_units.first().id == u2.id

    def test_meta_ordering_by_building_name_then_unit_number(self, owner):
        b1 = Building.objects.create(name="Alpha", address="a", owner=owner)
        b2 = Building.objects.create(name="Beta", address="b", owner=owner)
        # Mélange d'unit_number pour vérifier le tri lexical
        RealEstateUnit.objects.create(building=b2, unit_type='apartment', unit_number='2', size_m2=20, monthly_rent=200)
        RealEstateUnit.objects.create(building=b1,
                                      unit_type='apartment',
                                      unit_number='10',
                                      size_m2=20,
                                      monthly_rent=200
                                      )
        RealEstateUnit.objects.create(building=b1, unit_type='apartment', unit_number='2', size_m2=20, monthly_rent=200)
        names_pairs = [(u.building.name, u.unit_number) for u in RealEstateUnit.objects.all()]
        assert names_pairs == sorted(names_pairs)
