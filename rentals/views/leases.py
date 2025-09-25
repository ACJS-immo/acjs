from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from rentals.models import RealEstateUnit
from rentals.models.leases import LeaseContract


class LeaseDetailView(DetailView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_detail.html'

    def get_queryset(self):
        return LeaseContract.objects.select_related('real_estate_unit', 'tenant')


class LeaseListView(ListView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_list.html'
    context_object_name = 'leases'

    def get_queryset(self):
        return LeaseContract.objects.select_related('real_estate_unit', 'tenant').order_by('-start_date')


class LeaseCreateView(LoginRequiredMixin, CreateView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_form.html'
    fields = [
        'real_estate_unit', 'tenant', 'lease_type', 'start_date', 'end_date',
        'has_solidarity_clause', 'flat_rate_charges', 'deposit_amount',
        'status', 'contract_document', 'notes'
        ]
    success_url = reverse_lazy('rentals:leases_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter real_estate_units to only available ones
        form.fields['real_estate_unit'].queryset = RealEstateUnit.objects.filter(is_available=True)
        return form


class LeaseUpdateView(LoginRequiredMixin, UpdateView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_form.html'
    fields = [
        'real_estate_unit', 'tenant', 'lease_type', 'start_date', 'end_date',
        'has_solidarity_clause', 'flat_rate_charges', 'deposit_amount',
        'status', 'contract_document', 'notes'
        ]

    def get_success_url(self):
        return reverse('rentals:leases_detail', kwargs={'pk': self.object.pk})


class LeaseDeleteView(LoginRequiredMixin, DeleteView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_confirm_delete.html'
    success_url = reverse_lazy('rentals:leases_list')
