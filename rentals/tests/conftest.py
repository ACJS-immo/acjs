import pytest
from django.conf import settings

from rentals.models import Owner, Building, Property, Tenant, LeaseContract
from datetime import date, timedelta


def pytest_configure():
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            }
        }

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Active l'accès à la base de données pour tous les tests."""
    pass

@pytest.fixture
def owner():
    return Owner.objects.create(first_name="John", last_name="Doe", email="john@example.com")


@pytest.fixture
def building(owner):
    return Building.objects.create(name="Building A", address="123 Main St", owner=owner)


@pytest.fixture
def property(building):
    return Property.objects.create(
        building=building,
        property_type='apartment',
        unit_number="A1",
        size_m2=30.0,
        monthly_rent=800.0,
        specific_charges=50.0,
        is_available=True
        )


@pytest.fixture
def tenant():
    return Tenant.objects.create(first_name="Alice", last_name="Martin", email="alice@example.com")


@pytest.fixture
def active_lease(property, tenant):
    return LeaseContract.objects.create(
        property=property,
        tenant=tenant,
        lease_type='standard',
        start_date=date.today(),
        end_date=date.today() + timedelta(days=365),
        status='active'
        )
