from django.db.models import Prefetch
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from rentals.models import LeaseContract
from rentals.models.tenants import Tenant

class TenantListView(LoginRequiredMixin, ListView):
    model = Tenant
    template_name = 'rentals/tenants/tenant_list.html'
    context_object_name = 'tenants'
    paginate_by = 10

    def get_queryset(self):
        """Optimise les requêtes avec prefetch_related."""
        return Tenant.objects.prefetch_related(
            Prefetch(
                'lease_contracts',
                queryset=LeaseContract.objects.select_related('property'),
                to_attr='prefetched_leases'
                )
            )

class TenantDetailView(LoginRequiredMixin, DetailView):
    model = Tenant
    template_name = 'rentals/tenants/tenant_detail.html'

    def get_queryset(self):
        """Optimise les requêtes avec prefetch_related."""
        return Tenant.objects.prefetch_related(
            Prefetch(
                'lease_contracts',
                queryset=LeaseContract.objects.select_related('property', 'tenant'),
                to_attr='prefetched_leases'  # Stocke les baux préchargés dans cet attribut
                )
            )


class TenantCreateView(LoginRequiredMixin, CreateView):
    model = Tenant
    template_name = 'rentals/tenants/tenant_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'id_document', 'emergency_contact', 'notes']
    success_url = reverse_lazy('rentals:tenants_list')

class TenantUpdateView(LoginRequiredMixin, UpdateView):
    model = Tenant
    template_name = 'rentals/tenants/tenant_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'id_document', 'emergency_contact', 'notes']

    def get_success_url(self):
        return reverse('rentals:tenants_detail', kwargs={'pk': self.object.pk})

class TenantDeleteView(LoginRequiredMixin, DeleteView):
    model = Tenant
    template_name = 'rentals/tenants/tenant_confirm_delete.html'
    success_url = reverse_lazy('rentals:tenants_list')
