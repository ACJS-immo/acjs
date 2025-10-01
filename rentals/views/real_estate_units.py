from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.db.models import Prefetch

from rentals.models import RealEstateUnit, LeaseContract


class RealEstateUnitDetailView(DetailView):  # ✅ Renommé
    model = RealEstateUnit  # ✅ Mis à jour
    template_name = 'rentals/real_estate_units/real_estate_unit_detail.html'  # ✅ Corrigé
    context_object_name = 'real_estate_unit'

    def get_queryset(self):
        return RealEstateUnit.objects.prefetch_related(  # ✅ Mis à jour
            Prefetch(
                'lease_contracts',
                queryset=LeaseContract.objects.select_related('tenant'),
                to_attr='prefetched_leases'
            )
        ).select_related('building', 'owner')

class RealEstateUnitListView(ListView):
    model = RealEstateUnit
    template_name = 'rentals/real_estate_units/real_estate_unit_list.html'
    context_object_name = 'real_estate_units'
    paginate_by = 10

    def get_queryset(self):
        return RealEstateUnit.objects.select_related('building', 'owner')


class RealEstateUnitCreateView(LoginRequiredMixin, CreateView):
    model = RealEstateUnit
    template_name = 'rentals/real_estate_units/real_estate_unit_form.html'
    fields = [
        'building', 'owner', 'unit_type', 'unit_number',
        'size_m2', 'monthly_rent', 'specific_charges', 'is_available', 'description'
        ]
    success_url = reverse_lazy('rentals:real_estate_unit_list')


class RealEstateUnitUpdateView(LoginRequiredMixin, UpdateView):
    model = RealEstateUnit
    template_name = 'rentals/real_estate_units/real_estate_unit_form.html'
    fields = [
        'building', 'owner', 'unit_type', 'unit_number',
        'size_m2', 'monthly_rent', 'specific_charges', 'is_available', 'description'
        ]

    def get_success_url(self):
        return reverse('rentals:real_estate_unit_detail', kwargs={'pk': self.object.pk})


class RealEstateUnitDeleteView(LoginRequiredMixin, DeleteView):
    model = RealEstateUnit
    template_name = 'rentals/real_estate_units/real_estate_unit_confirm_delete.html'
    success_url = reverse_lazy('rentals:real_estate_units_list')
