from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from rentals.models.leases import LeaseContract
from rentals.models.properties import Property

class LeaseListView(LoginRequiredMixin, ListView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_list.html'
    context_object_name = 'leases'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().select_related('property', 'tenant')

class LeaseDetailView(LoginRequiredMixin, DetailView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_detail.html'

class LeaseCreateView(LoginRequiredMixin, CreateView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_form.html'
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
    template_name = 'rentals/leases/lease_form.html'
    fields = [
        'property', 'tenant', 'lease_type', 'start_date', 'end_date',
        'has_solidarity_clause', 'flat_rate_charges', 'deposit_amount',
        'status', 'contract_document', 'notes'
    ]

    def get_success_url(self):
        return reverse('leases:detail', kwargs={'pk': self.object.pk})

class LeaseDeleteView(LoginRequiredMixin, DeleteView):
    model = LeaseContract
    template_name = 'rentals/leases/lease_confirm_delete.html'
    success_url = reverse_lazy('leases:list')
