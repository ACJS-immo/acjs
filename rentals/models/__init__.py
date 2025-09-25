# Importe tous les modèles pour que Django les trouve automatiquement
from .owners import Owner
from .buildings import Building, ChargeDistribution
from .real_estate_units import RealEstateUnit
from .tenants import Tenant
from .leases import LeaseContract
