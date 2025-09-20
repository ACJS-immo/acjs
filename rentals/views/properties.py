from django.db.models import Prefetch
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from rentals.models import LeaseContract
from rentals.models.properties import Property


class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'rentals/properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 10


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'rentals/properties/property_detail.html'

    def get_queryset(self):
        return Property.objects.prefetch_related(
            Prefetch(
                'lease_contracts',
                queryset=LeaseContract.objects.select_related('tenant', 'property'),
                to_attr='prefetched_leases'  # Stocke les baux préchargés dans cet attribut
                )
            )


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    template_name = 'rentals/properties/property_form.html'
    fields = [
        'building', 'owner', 'property_type', 'unit_number',
        'size_m2', 'monthly_rent', 'specific_charges', 'is_available', 'description'
        ]
    success_url = reverse_lazy('rentals:properties_list')


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    template_name = 'rentals/properties/property_form.html'
    fields = [
        'building', 'owner', 'property_type', 'unit_number',
        'size_m2', 'monthly_rent', 'specific_charges', 'is_available', 'description'
        ]

    def get_success_url(self):
        return reverse('rentals:properties_detail', kwargs={'pk': self.object.pk})


class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property
    template_name = 'rentals/properties/property_confirm_delete.html'
    success_url = reverse_lazy('rentals:properties_list')
