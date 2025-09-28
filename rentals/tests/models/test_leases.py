import pytest
from datetime import date, timedelta

from rentals.models import LeaseContract, RealEstateUnit, Building, Owner, Tenant
from rentals.models.leases import LeaseType


@pytest.mark.django_db
class TestLeaseContractModel:
    def _make_unit(self):
        idx = Owner.objects.count() + 1
        owner = Owner.objects.create(first_name="John", last_name="Doe", email=f"john{idx}@example.com")
        b = Building.objects.create(name="Bloc A", address="1 rue A", owner=owner)
        return RealEstateUnit.objects.create(
            building=b,
            unit_type='apartment',
            unit_number='A1',
            size_m2=40,
            monthly_rent=600,
            specific_charges=50,
            is_available=True,
        )

    def _make_tenant(self):
        return Tenant.objects.create(first_name="Alice", last_name="Martin", email="alice@example.com")

    def test_creation_and_str(self):
        unit = self._make_unit()
        tenant = self._make_tenant()
        lease = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            lease_type=LeaseType.STANDARD,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            status='active'
        )
        s = str(lease)
        assert "Lease" in s
        assert unit.unit_number in s
        # Le __str__ inclut aussi le locataire
        assert tenant.last_name in s

    def test_total_monthly_amount_standard(self):
        unit = self._make_unit()  # 600 + 50 => 650
        tenant = self._make_tenant()
        lease = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            lease_type=LeaseType.STANDARD,
            start_date=date.today(),
            status='active'
        )
        from decimal import Decimal
        assert lease.total_monthly_amount == Decimal('650.00')

    def test_total_monthly_amount_colocation_with_flat_rate(self):
        unit = self._make_unit()  # 600 + flat 80 => 680
        tenant = self._make_tenant()
        lease = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            lease_type=LeaseType.COLOCATION,
            flat_rate_charges=80,
            start_date=date.today(),
            status='active'
        )
        from decimal import Decimal
        assert lease.total_monthly_amount == Decimal('680.00')

    def test_is_active_true_and_false(self):
        unit = self._make_unit()
        tenant = self._make_tenant()
        # Actif aujourd'hui
        active = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=30),
            status='active'
        )
        assert active.is_active is True
        # Brouillon
        draft = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            start_date=active.end_date + timedelta(days=1),
            end_date=active.end_date + timedelta(days=31),
            status='draft'
        )
        assert draft.is_active is False
        # Terminé hier
        terminated = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            start_date=date.today() - timedelta(days=60),
            end_date=(active.start_date - timedelta(days=1)),
            status='terminated'
        )
        assert terminated.is_active is False

    def test_duration_in_months(self):
        unit = self._make_unit()
        tenant = self._make_tenant()
        lease = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            start_date=date.today() - timedelta(days=90),
            end_date=date.today(),
            status='active'
        )
        # 90 // 30 = 3
        assert lease.duration_in_months == 3
        # Sans end_date => None
        # Crée un bail sans date de fin sur une autre unité pour éviter tout chevauchement
        unit2 = self._make_unit()
        open_ended = LeaseContract.objects.create(
            real_estate_unit=unit2,
            tenant=tenant,
            start_date=date.today() + timedelta(days=1),
            end_date=None,
            status='active'
        )
        assert open_ended.duration_in_months is None

    def test_remaining_days(self):
        unit = self._make_unit()
        tenant = self._make_tenant()
        # Bail actif qui finit dans 10 jours => 10
        active = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=10),
            status='active'
        )
        assert active.remaining_days in (10, 9)  # tolérance si la date change entre les assertions
        # Non actif => None
        draft = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            start_date=active.end_date + timedelta(days=1),
            end_date=active.end_date + timedelta(days=11),
            status='draft'
        )
        assert draft.remaining_days is None
        # Sans end_date => None
        # Crée un bail sans date de fin sur une autre unité pour éviter tout chevauchement
        unit3 = self._make_unit()
        no_end = LeaseContract.objects.create(
            real_estate_unit=unit3,
            tenant=tenant,
            start_date=date.today(),
            end_date=None,
            status='active'
        )
        assert no_end.remaining_days is None

    def test_related_names_from_unit_and_tenant(self):
        unit = self._make_unit()
        tenant = self._make_tenant()
        assert unit.lease_contracts.count() == 0
        assert tenant.lease_contracts.count() == 0
        LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status='active'
        )
        assert unit.lease_contracts.count() == 1
        assert tenant.lease_contracts.count() == 1

    def test_meta_ordering_by_start_date_desc(self):
        unit = self._make_unit()
        tenant = self._make_tenant()
        older = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() - timedelta(days=2),
            status='active'
        )
        newer = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=20),
            status='active'
        )
        ids = [l.id for l in LeaseContract.objects.all()]
        assert ids[0] == newer.id
        assert ids[1] == older.id

    def test_signals_update_unit_availability_on_save_and_delete(self):
        unit = self._make_unit()
        tenant = self._make_tenant()
        # Création d'un bail actif => l'unité devient indisponible
        lease = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status='active'
        )
        unit.refresh_from_db()
        assert unit.is_available is False
        # Suppression du seul bail actif => redevient disponible
        lease.delete()
        unit.refresh_from_db()
        assert unit.is_available is True

        # Cas avec deux baux: si un est supprimé, mais l'autre actif existe, reste indisponible
        lease1 = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=tenant,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status='active'
        )
        lease2 = LeaseContract.objects.create(
            real_estate_unit=unit,
            tenant=Tenant.objects.create(first_name="Bob", last_name="Durand", email="bob2@example.com"),
            start_date=lease1.end_date + timedelta(days=1),
            end_date=lease1.end_date + timedelta(days=15),
            status='active'
        )
        unit.refresh_from_db()
        assert unit.is_available is False
        lease1.delete()
        unit.refresh_from_db()
        assert unit.is_available is False  # Toujours indispo car lease2 est actif
        lease2.delete()
        unit.refresh_from_db()
        assert unit.is_available is True
