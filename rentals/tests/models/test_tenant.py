from datetime import date, timedelta

import pytest

from rentals.models import Tenant, LeaseContract, RealEstateUnit, Building, Owner


@pytest.mark.django_db
class TestTenantModel:
    """Tests unitaires pour le modèle Tenant et ses propriétés."""

    def test_tenant_creation_and_str(self):
        t = Tenant.objects.create(first_name="Ana", last_name="Pop", email="ana@example.com")
        assert t.first_name == "Ana"
        assert t.last_name == "Pop"
        assert str(t) == "Pop Ana"

    def test_active_leases_with_no_leases(self, tenant):
        """Aucun bail: toutes les métriques doivent être à 0/False."""
        # Sans prefetch: active_leases est un QuerySet
        qs = tenant.active_leases
        # Assure que l'objet supporte len() même si c'est un QuerySet
        assert len(qs) == 0
        # Et que les compteurs/propriétés concordent
        assert tenant.has_active_lease is False
        assert tenant.total_leases_count == 0
        assert tenant.active_leases_count == 0

    def _make_unit(self, owner=None, building=None):
        if not owner:
            owner = Owner.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        if not building:
            building = Building.objects.create(name="Bloc A", address="1 rue A", owner=owner)
        return RealEstateUnit.objects.create(
            building=building,
            unit_type='apartment',
            unit_number='A1',
            size_m2=40,
            monthly_rent=600,
            is_available=True,
        )

    def test_active_leases_with_active_lease(self, tenant):
        unit = self._make_unit()
        lease = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            status='active'
        )
        # Sans prefetch: active_leases est un QuerySet
        qs = tenant.active_leases
        assert hasattr(qs, 'count')
        assert qs.count() == 1
        assert tenant.has_active_lease is True
        assert tenant.total_leases_count == 1
        assert tenant.active_leases_count == 1
        assert qs.first().id == lease.id

    def test_active_leases_with_inactive_leases(self, tenant):
        unit = self._make_unit()
        LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today() - timedelta(days=365),
            end_date=date.today() - timedelta(days=1),
            status='terminated'
        )
        qs = tenant.active_leases
        assert hasattr(qs, 'count')
        assert qs.count() == 0
        assert tenant.has_active_lease is False
        assert tenant.total_leases_count == 1
        assert tenant.active_leases_count == 0

    def test_active_leases_with_prefetched_data(self, tenant):
        unit = self._make_unit()
        active = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            status='active'
        )
        # Ajoute aussi un bail terminé pour vérifier les compteurs
        LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today() - timedelta(days=400),
            end_date=date.today() - timedelta(days=200),
            status='terminated'
        )
        # Simule prefetch_related
        tenant.prefetched_leases = list(tenant.lease_contracts.all())

        # Avec prefetch: active_leases est une liste filtrée
        active_list = tenant.active_leases
        assert isinstance(active_list, list)
        assert len(active_list) == 1
        assert active_list[0].id == active.id
        # Compteurs utilisant prefetched_leases
        assert tenant.has_active_lease is True
        assert tenant.total_leases_count == 2
        assert tenant.active_leases_count == 1

    def test_related_name_lease_contracts(self, tenant):
        unit = self._make_unit()
        assert tenant.lease_contracts.count() == 0
        LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            status='active'
        )
        assert tenant.lease_contracts.count() == 1
