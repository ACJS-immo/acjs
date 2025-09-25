import pytest
from datetime import date, timedelta
from rentals.models import Tenant, LeaseContract, Property, Building, Owner

@pytest.mark.django_db
class TestTenantModel:
    """Tests unitaires pour le modèle Tenant et ses propriétés."""

    def test_active_leases_with_no_leases(self, tenant):
        """Test active_leases quand il n'y a pas de baux."""
        assert tenant.active_leases.count() == 0
        assert tenant.has_active_lease is False
        assert tenant.total_leases_count == 0
        assert tenant.active_leases_count == 0

    def test_active_leases_with_active_lease(self, tenant, property):
        """Test active_leases avec un bail actif."""
        lease = LeaseContract.objects.create(
            property=property,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            status='active'
        )
        assert tenant.active_leases.count() == 1
        assert tenant.has_active_lease is True
        assert tenant.total_leases_count == 1
        assert tenant.active_leases_count == 1
        assert tenant.active_leases.first() == lease

    def test_active_leases_with_inactive_leases(self, tenant, property):
        """Test active_leases avec des baux inactifs."""
        LeaseContract.objects.create(
            property=property,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today() - timedelta(days=365),
            end_date=date.today() - timedelta(days=1),
            status='terminated'
        )
        assert tenant.active_leases.count() == 0
        assert tenant.has_active_lease is False
        assert tenant.total_leases_count == 1
        assert tenant.active_leases_count == 0

    def test_active_leases_with_prefetched_data(self, tenant, property):
        """Test active_leases avec des données préchargées."""
        lease = LeaseContract.objects.create(
            property=property,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            status='active'
        )

        # Simule prefetch_related en ajoutant manuellement l'attribut
        tenant.prefetched_leases = list(tenant.lease_contracts.all())

        assert tenant.active_leases.count() == 1
        assert tenant.has_active_lease is True
        assert tenant.total_leases_count == 1
        assert tenant.active_leases_count == 1
        assert tenant.active_leases.first() == lease
