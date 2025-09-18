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
