from django.db import models
from django.db.models import Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from rentals.models.buildings import Building

class BuildingListView(LoginRequiredMixin, ListView):
    model = Building
    template_name = 'rentals/buildings/building_list.html'
    context_object_name = 'buildings'
    paginate_by = 10

class BuildingDetailView(LoginRequiredMixin, DetailView):
    model = Building
    template_name = 'rentals/buildings/building_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = self.object.properties.all()
        return context

    def get_queryset(self):
        return Building.objects.annotate(
            available_properties_count=Count('properties', filter=models.Q(properties__is_available=True)),
            total_properties_count=Count('properties'),
            rented_properties_count=Count('properties', filter=models.Q(properties__is_available=False))
            )

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
