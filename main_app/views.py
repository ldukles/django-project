from django.shortcuts import render
from .models import Observation

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
