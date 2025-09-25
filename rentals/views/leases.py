from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from rentals.models.leases import LeaseContract
from rentals.models.properties import Property

from django.views.generic import DetailView, ListView
from django.db.models import Prefetch

class LeaseDetailView(DetailView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_detail.html'

    def get_queryset(self):
        return LeaseContract.objects.select_related('property', 'tenant')

class LeaseListView(ListView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_list.html'
    context_object_name = 'leases'

    def get_queryset(self):
        return LeaseContract.objects.select_related('property', 'tenant').order_by('-start_date')


class LeaseCreateView(LoginRequiredMixin, CreateView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_form.html'
    fields = [
        'property', 'tenant', 'lease_type', 'start_date', 'end_date',
        'has_solidarity_clause', 'flat_rate_charges', 'deposit_amount',
        'status', 'contract_document', 'notes'
    ]
    success_url = reverse_lazy('rentals:leases_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter properties to only available ones
        form.fields['property'].queryset = Property.objects.filter(is_available=True)
        return form

class LeaseUpdateView(LoginRequiredMixin, UpdateView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_form.html'
    fields = [
        'property', 'tenant', 'lease_type', 'start_date', 'end_date',
        'has_solidarity_clause', 'flat_rate_charges', 'deposit_amount',
        'status', 'contract_document', 'notes'
    ]

    def get_success_url(self):
        return reverse('rentals:leases_detail', kwargs={'pk': self.object.pk})

class LeaseDeleteView(LoginRequiredMixin, DeleteView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_confirm_delete.html'
    success_url = reverse_lazy('rentals:leases_list')
