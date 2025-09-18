# Importe tous les modèles pour que Django les trouve automatiquement
from .owners import Owner
from .buildings import Building, ChargeDistribution
from .properties import Property
from .tenants import Tenant
from .leases import LeaseContract
