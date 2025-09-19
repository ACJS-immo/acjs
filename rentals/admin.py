from django.contrib import admin
from rentals.models.owners import Owner
from rentals.models.buildings import Building, ChargeDistribution
from rentals.models.properties import Property
from rentals.models.tenants import Tenant
from rentals.models.leases import LeaseContract

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone')
    search_fields = ('last_name', 'first_name', 'email')
    list_filter = ('last_name',)

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'total_general_charges', 'has_individual_meters', 'owner')
    search_fields = ('name', 'address')
    list_filter = ('has_individual_meters', 'owner')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('building', 'property_type', 'unit_number', 'size_m2', 'monthly_rent', 'is_available', 'current_owner')
    search_fields = ('building__name', 'unit_number')
    list_filter = ('property_type', 'is_available', 'building')

    def current_owner(self, obj):
        return obj.current_owner()
    current_owner.short_description = 'Owner'

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone')
    search_fields = ('last_name', 'first_name', 'email')
    list_filter = ('last_name',)

@admin.register(LeaseContract)
class LeaseContractAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'start_date', 'end_date', 'status', 'total_monthly_amount')
    search_fields = ('property__unit_number', 'tenant__last_name', 'tenant__first_name')
    list_filter = ('status', 'lease_type', 'start_date', 'property__building__name')

    def total_monthly_amount(self, obj):
        return obj.total_monthly_amount()
    total_monthly_amount.short_description = 'Monthly Amount ($)'

@admin.register(ChargeDistribution)
class ChargeDistributionAdmin(admin.ModelAdmin):
    list_display = ('building', 'property', 'distribution_percentage', 'start_date', 'end_date')
    search_fields = ('building__name', 'property__unit_number')
    list_filter = ('building', 'start_date')
