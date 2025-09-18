from django.shortcuts import render
from .models import LeaseContract
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Owner

class OwnerListView(LoginRequiredMixin, ListView):
    model = Owner
    template_name = 'owners/owner_list.html'
    context_object_name = 'owners'
    paginate_by = 10

class OwnerDetailView(LoginRequiredMixin, DetailView):
    model = Owner
    template_name = 'owners/owner_detail.html'

class OwnerCreateView(LoginRequiredMixin, CreateView):
    model = Owner
    template_name = 'owners/owner_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'tax_number', 'notes']
    success_url = reverse_lazy('owners:list')

class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    model = Owner
    template_name = 'owners/owner_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'tax_number', 'notes']

    def get_success_url(self):
        return reverse('owners:detail', kwargs={'pk': self.object.pk})

class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    model = Owner
    template_name = 'owners/owner_confirm_delete.html'
    success_url = reverse_lazy('owners:list')

from .models import Building

class BuildingListView(LoginRequiredMixin, ListView):
    model = Building
    template_name = 'buildings/building_list.html'
    context_object_name = 'buildings'
    paginate_by = 10

class BuildingDetailView(LoginRequiredMixin, DetailView):
    model = Building
    template_name = 'buildings/building_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = self.object.properties.all()
        return context

class BuildingCreateView(LoginRequiredMixin, CreateView):
    model = Building
    template_name = 'buildings/building_form.html'
    fields = ['name', 'address', 'total_general_charges', 'has_individual_meters', 'owner']
    success_url = reverse_lazy('buildings:list')

class BuildingUpdateView(LoginRequiredMixin, UpdateView):
    model = Building
    template_name = 'buildings/building_form.html'
    fields = ['name', 'address', 'total_general_charges', 'has_individual_meters', 'owner']

    def get_success_url(self):
        return reverse('buildings:detail', kwargs={'pk': self.object.pk})

class BuildingDeleteView(LoginRequiredMixin, DeleteView):
    model = Building
    template_name = 'buildings/building_confirm_delete.html'
    success_url = reverse_lazy('buildings:list')

from .models import Property

class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 10

class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = 'properties/property_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lease_contracts'] = self.object.lease_contracts.filter(status='active')
        return context

class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    template_name = 'properties/property_form.html'
    fields = [
        'building', 'owner', 'property_type', 'unit_number',
        'size_m2', 'monthly_rent', 'specific_charges', 'is_available', 'description'
    ]
    success_url = reverse_lazy('properties:list')

class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    template_name = 'properties/property_form.html'
    fields = [
        'building', 'owner', 'property_type', 'unit_number',
        'size_m2', 'monthly_rent', 'specific_charges', 'is_available', 'description'
    ]

    def get_success_url(self):
        return reverse('properties:detail', kwargs={'pk': self.object.pk})

class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property
    template_name = 'properties/property_confirm_delete.html'
    success_url = reverse_lazy('properties:list')

from .models import Tenant

class TenantListView(LoginRequiredMixin, ListView):
    model = Tenant
    template_name = 'tenants/tenant_list.html'
    context_object_name = 'tenants'
    paginate_by = 10

class TenantDetailView(LoginRequiredMixin, DetailView):
    model = Tenant
    template_name = 'tenants/tenant_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_leases'] = self.object.lease_contracts.filter(status='active')
        return context

class TenantCreateView(LoginRequiredMixin, CreateView):
    model = Tenant
    template_name = 'tenants/tenant_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'id_document', 'emergency_contact', 'notes']
    success_url = reverse_lazy('tenants:list')

class TenantUpdateView(LoginRequiredMixin, UpdateView):
    model = Tenant
    template_name = 'tenants/tenant_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'id_document', 'emergency_contact', 'notes']

    def get_success_url(self):
        return reverse('tenants:detail', kwargs={'pk': self.object.pk})

class TenantDeleteView(LoginRequiredMixin, DeleteView):
    model = Tenant
    template_name = 'tenants/tenant_confirm_delete.html'
    success_url = reverse_lazy('tenants:list')
from .models import LeaseContract

class LeaseListView(LoginRequiredMixin, ListView):
    model = LeaseContract
    template_name = 'leases/lease_list.html'
    context_object_name = 'leases'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().select_related('property', 'tenant')

class LeaseDetailView(LoginRequiredMixin, DetailView):
    model = LeaseContract
    template_name = 'leases/lease_detail.html'

class LeaseCreateView(LoginRequiredMixin, CreateView):
    model = LeaseContract
    template_name = 'leases/lease_form.html'
    fields = [
        'property', 'tenant', 'lease_type', 'start_date', 'end_date',
        'has_solidarity_clause', 'flat_rate_charges', 'deposit_amount',
        'status', 'contract_document', 'notes'
    ]
    success_url = reverse_lazy('leases:list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter properties to only available ones
        form.fields['property'].queryset = Property.objects.filter(is_available=True)
        return form

class LeaseUpdateView(LoginRequiredMixin, UpdateView):
    model = LeaseContract
    template_name = 'leases/lease_form.html'
    fields = [
        'property', 'tenant', 'lease_type', 'start_date', 'end_date',
        'has_solidarity_clause', 'flat_rate_charges', 'deposit_amount',
        'status', 'contract_document', 'notes'
    ]

    def get_success_url(self):
        return reverse('leases:detail', kwargs={'pk': self.object.pk})

class LeaseDeleteView(LoginRequiredMixin, DeleteView):
    model = LeaseContract
    template_name = 'leases/lease_confirm_delete.html'
    success_url = reverse_lazy('leases:list')
