from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Observation
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.http import HttpResponse

# HOME VIEW
def home(request):
  return render(request, 'home.html')

# ABOUT VIEW
def about(request):
  return render(request, 'about.html')

def observations_index(request):
    observations = Observation.objects.all()
    return render(request, 'observations/index.html', { 'observations': observations })

def observations_detail(request, observation_id):
  observation = Observation.objects.get(id=observation_id)
  return render(request, 'observations/detail.html', { 'observation': observation })


class ObservationCreate(CreateView):
  model = Observation
  fields = ['name', 'sciname', 'amount', 'date', 'location', 'description', 'details']


class ObservationUpdate(UpdateView):
  model = Observation
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['name', 'sciname', 'amount', 'date', 'location', 'description', 'details']

class ObservationDelete(DeleteView):
  model = Observation
  success_url = '/observations/'