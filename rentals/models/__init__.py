# Importe tous les modèles pour que Django les trouve automatiquement
from .buildings import Building
from .leases import LeaseContract
from .owners import Owner
from .real_estate_units import RealEstateUnit
from .tenants import Tenant

__all__ = ['Owner', 'Building', 'RealEstateUnit', 'Tenant']