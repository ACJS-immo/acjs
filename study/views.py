from django.views.generic import CreateView, DetailView
from .models import RealEstateProperty
from .forms import RealEstatePropertyForm

class RealEstatePropertyCreateView(CreateView):
    model = RealEstateProperty
    form_class = RealEstatePropertyForm
    template_name = 'study/property_form.html'
    success_url = '/study/success/'

class RealEstatePropertyDetailView(DetailView):
    model = RealEstateProperty
    template_name = 'study/property_detail.html'
