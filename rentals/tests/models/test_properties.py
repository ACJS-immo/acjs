import pytest
from django.utils import timezone
from datetime import date, timedelta
from rentals.models import Property, LeaseContract

@pytest.mark.django_db
class TestPropertyModel:
    """Tests unitaires pour le modèle Property."""

    def test_property_creation(self, building):
        """Test la création d'une propriété."""
        property = Property.objects.create(
            building=building,
            property_type='apartment',
            unit_number="A1",
            size_m2=50.0,
            monthly_rent=800.0,
            specific_charges=50.0,
            is_available=True
        )
        assert property.building == building
        assert property.property_type == 'apartment'
        assert property.unit_number == "A1"
        assert property.size_m2 == 50.0
        assert property.monthly_rent == 800.0
        assert property.specific_charges == 50.0
        assert property.is_available is True
        assert property.current_owner() == building.owner

    def test_total_monthly_cost(self, property):
        """Test la méthode total_monthly_cost."""
        assert property.total_monthly_cost() == 850.0  # 800 (loyer) + 50 (charges)

    def test_active_leases_with_no_leases(self, property):
        """Test active_leases quand il n'y a pas de baux."""
        assert property.active_leases.count() == 0
        assert property.has_active_lease is False

    def test_active_leases_with_active_lease(self, property, tenant, active_lease):
        """Test active_leases avec un bail actif."""
        assert property.active_leases.count() == 1
        assert property.has_active_lease is True
        assert property.active_leases.first().tenant == tenant

    def test_active_leases_with_inactive_leases(self, property, tenant):
        """Test active_leases avec des baux inactifs."""
        # Créer un bail terminé
        LeaseContract.objects.create(
            property=property,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today() - timedelta(days=365),
            end_date=date.today() - timedelta(days=1),
            status='terminated'
        )
        assert property.active_leases.count() == 0
        assert property.has_active_lease is False

    def test_property_available_status(self, property, tenant, active_lease):
        """Test le champ is_available en fonction des baux."""
        property.refresh_from_db()
        assert property.is_available is False  # Doit être False car il y a un bail actif

    def test_property_get_absolute_url(self, property):
        """Test la méthode get_absolute_url."""
        from django.urls import reverse
        assert property.get_absolute_url() == reverse('rentals:properties_detail', args=[property.pk])
