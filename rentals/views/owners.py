from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from rentals.models.owners import Owner

from django.views.generic import DetailView, ListView
from django.db.models import Prefetch

class OwnerDetailView(DetailView):
    model = Owner
    template_name = 'rentals/owners/owner_detail.html'

    def get_queryset(self):
        return Owner.objects.prefetch_related(
            Prefetch('buildings', queryset=Building.objects.all(), to_attr='prefetched_buildings'),
            Prefetch('real_estate_units', queryset=Property.objects.all(), to_attr='prefetched_properties')
        )

class OwnerListView(ListView):
    model = Owner
    template_name = 'rentals/owners/owner_list.html'
    context_object_name = 'owners'

    def get_queryset(self):
        return Owner.objects.prefetch_related(
            Prefetch('buildings', queryset=Building.objects.all(), to_attr='prefetched_buildings')
        )


class OwnerCreateView(LoginRequiredMixin, CreateView):
    model = Owner
    template_name = 'rentals/owners/owner_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'tax_number', 'notes']
    success_url = reverse_lazy('rentals:owners_list')

class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    model = Owner
    template_name = 'rentals/owners/owner_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'tax_number', 'notes']

    def get_success_url(self):
        return reverse('rentals:owners_detail', kwargs={'pk': self.object.pk})

class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    model = Owner
    template_name = 'rentals/owners/owner_confirm_delete.html'
    success_url = reverse_lazy('rentals:owners_list')
