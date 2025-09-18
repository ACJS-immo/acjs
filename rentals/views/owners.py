from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rentals.models.owners import Owner

class OwnerListView(LoginRequiredMixin, ListView):
    model = Owner
    template_name = 'rentals/owners/owner_list.html'
    context_object_name = 'owners'
    paginate_by = 10

class OwnerDetailView(LoginRequiredMixin, DetailView):
    model = Owner
    template_name = 'rentals/owners/owner_detail.html'

class OwnerCreateView(LoginRequiredMixin, CreateView):
    model = Owner
    template_name = 'rentals/owners/owner_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'tax_number', 'notes']
    success_url = reverse_lazy('owners:list')

class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    model = Owner
    template_name = 'rentals/owners/owner_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'tax_number', 'notes']

    def get_success_url(self):
        return reverse('owners:detail', kwargs={'pk': self.object.pk})

class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    model = Owner
    template_name = 'rentals/owners/owner_confirm_delete.html'
    success_url = reverse_lazy('owners:list')
