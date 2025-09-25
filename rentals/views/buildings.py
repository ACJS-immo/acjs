from django.db import models
from django.db.models import Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from rentals.models.buildings import Building

from django.views.generic import DetailView, ListView
from django.db.models import Prefetch

class BuildingDetailView(DetailView):
    model = Building
    template_name = 'rentals/buildings/building_detail.html'

    def get_queryset(self):
        return Building.objects.prefetch_related(
            Prefetch(
                'properties',
                queryset=Property.objects.all(),
                to_attr='prefetched_properties'
            ),
            Prefetch(
                'charge_distributions',
                queryset=ChargeDistribution.objects.all(),
                to_attr='prefetched_charge_distributions'
            )
        ).select_related('owner')

class BuildingListView(ListView):
    model = Building
    template_name = 'rentals/buildings/building_list.html'
    context_object_name = 'buildings'

    def get_queryset(self):
        return Building.objects.select_related('owner')

class BuildingCreateView(LoginRequiredMixin, CreateView):
    model = Building
    template_name = 'rentals/buildings/building_form.html'
    fields = ['name', 'address', 'total_general_charges', 'has_individual_meters', 'owner']
    success_url = reverse_lazy('rentals:buildings_list')

class BuildingUpdateView(LoginRequiredMixin, UpdateView):
    model = Building
    template_name = 'rentals/buildings/building_form.html'
    fields = ['name', 'address', 'total_general_charges', 'has_individual_meters', 'owner']

    def get_success_url(self):
        return reverse('rentals:buildings_detail', kwargs={'pk': self.object.pk})

class BuildingDeleteView(LoginRequiredMixin, DeleteView):
    model = Building
    template_name = 'rentals/buildings/building_confirm_delete.html'
    success_url = reverse_lazy('rentals:buildings_list')
