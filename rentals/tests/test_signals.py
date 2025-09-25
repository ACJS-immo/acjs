import pytest
from django.test import TestCase
from rentals.models import Property, LeaseContract, Tenant, Owner, Building
from django.utils import timezone

class LeaseContractSignalsTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(first_name="Jean", last_name="Dupont")
        self.building = Building.objects.create(name="Test Building", owner=self.owner)
        self.property = Property.objects.create(
            building=self.building,
            property_type='apartment',
            unit_number="A1",
            monthly_rent=800,
            is_available=True
        )
        self.tenant = Tenant.objects.create(first_name="Alice", last_name="Martin")

    def test_lease_creation_updates_property_availability(self):
        lease = LeaseContract.objects.create(
            property=self.property,
            tenant=self.tenant,
            lease_type='standard',
            start_date=timezone.now().date(),
            status='active'
        )
        self.property.refresh_from_db()
        self.assertFalse(self.property.is_available, "Property should be unavailable after lease creation")

    def test_lease_deletion_updates_property_availability(self):
        lease = LeaseContract.objects.create(
            property=self.property,
            tenant=self.tenant,
            lease_type='standard',
            start_date=timezone.now().date(),
            status='active'
        )
        lease.delete()
        self.property.refresh_from_db()
        self.assertTrue(self.property.is_available, "Property should be available after lease deletion")

@pytest.mark.django_db
class TestPropertySignals:
    """Tests pour les signaux liés au modèle Property."""

    def test_property_available_status_updated_on_lease_creation(self):
        """Test que is_available est mis à False quand un bail est créé."""
        owner = Owner.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        building = Building.objects.create(name="Building A", address="123 Main St", owner=owner)
        property = Property.objects.create(
            building=building,
            property_type='apartment',
            unit_number="A1",
            size_m2=50.0,
            monthly_rent=800.0,
            is_available=True
        )
        tenant = Tenant.objects.create(first_name="Alice", last_name="Martin", email="alice@example.com")
        LeaseContract.objects.create(
            property=property,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            status='active'
        )
        property.refresh_from_db()  # Rafraîchit depuis la base de données
        assert property.is_available is False

    def test_property_available_status_updated_on_lease_deletion(self):
        """Test que is_available est mis à True quand un bail est supprimé."""
        owner = Owner.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        building = Building.objects.create(name="Building A", address="123 Main St", owner=owner)
        property = Property.objects.create(
            building=building,
            property_type='apartment',
            unit_number="A1",
            size_m2=50.0,
            monthly_rent=800.0,
            is_available=True
        )
        tenant = Tenant.objects.create(first_name="Alice", last_name="Martin", email="alice@example.com")
        lease = LeaseContract.objects.create(
            property=property,
            tenant=tenant,
            lease_type='standard',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            status='active'
        )
        property.refresh_from_db()
        assert property.is_available is False

        lease.delete()
        property.refresh_from_db()
        assert property.is_available is True
