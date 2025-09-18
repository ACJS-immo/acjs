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

class BuildingCreateView(LoginRequiredMixin, CreateView):
    model = Building
    template_name = 'rentals/buildings/building_form.html'
    fields = ['name', 'address', 'total_general_charges', 'has_individual_meters', 'owner']
    success_url = reverse_lazy('buildings:list')

class BuildingUpdateView(LoginRequiredMixin, UpdateView):
    model = Building
    template_name = 'rentals/buildings/building_form.html'
    fields = ['name', 'address', 'total_general_charges', 'has_individual_meters', 'owner']

    def get_success_url(self):
        return reverse('buildings:detail', kwargs={'pk': self.object.pk})

class BuildingDeleteView(LoginRequiredMixin, DeleteView):
    model = Building
    template_name = 'rentals/buildings/building_confirm_delete.html'
    success_url = reverse_lazy('buildings:list')
