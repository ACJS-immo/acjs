from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from rentals.models.tenants import Tenant

class TenantListView(LoginRequiredMixin, ListView):
    model = Tenant
    template_name = 'rentals/tenants/tenant_list.html'
    context_object_name = 'tenants'
    paginate_by = 10

class TenantDetailView(LoginRequiredMixin, DetailView):
    model = Tenant
    template_name = 'rentals/tenants/tenant_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_leases'] = self.object.lease_contracts.filter(status='active')
        return context

class TenantCreateView(LoginRequiredMixin, CreateView):
    model = Tenant
    template_name = 'rentals/tenants/tenant_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'id_document', 'emergency_contact', 'notes']
    success_url = reverse_lazy('tenants:list')

class TenantUpdateView(LoginRequiredMixin, UpdateView):
    model = Tenant
    template_name = 'rentals/tenants/tenant_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'id_document', 'emergency_contact', 'notes']

    def get_success_url(self):
        return reverse('tenants:detail', kwargs={'pk': self.object.pk})

class TenantDeleteView(LoginRequiredMixin, DeleteView):
    model = Tenant
    template_name = 'rentals/tenants/tenant_confirm_delete.html'
    success_url = reverse_lazy('tenants:list')
