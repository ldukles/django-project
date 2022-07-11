from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Observation
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from .models import Observation, Category

# HOME VIEW
def home(request):
  return render(request, 'home.html')

# ABOUT VIEW
def about(request):
  return render(request, 'about.html')

# OBSERVATION INDEX
def observations_index(request):
    observations = Observation.objects.all()
    return render(request, 'observations/index.html', { 'observations': observations })

# INDIVDUAL OBSERVATION DETAIL
def observations_detail(request, observation_id):
    observation = Observation.objects.get(id=observation_id)
    categorys_observation_doesnt_have = Category.objects.exclude(id__in = observation.categorys.all().values_list('id'))
    return render(request, 'observations/detail.html', {
        'observation': observation,
        'categorys': categorys_observation_doesnt_have
  })

# ASSOCIATING OBSERVATION WITH CATEGORY
def assoc_category(request, observation_id, category_id):
  Observation.objects.get(id=observation_id).categorys.add(category_id)
  return redirect('detail', observation_id=observation_id)


# DELETING CATEGORY FROM ASSOCIATED OBSERVATION
def assoc_category_delete(request, observation_id, category_id):
  Observation.objects.get(id=observation_id).categorys.remove(category_id)
  return redirect('detail', observation_id=observation_id)


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

class CategoryList(ListView):
  model = Category
  template_name = 'categorys/index.html'

class CategoryDetail(DetailView):
  model = Category
  template_name = 'categorys/detail.html'

class CategoryCreate(CreateView):
    model = Category
    fields = ['classification']


class CategoryUpdate(UpdateView):
    model = Category
    fields = ['classification']


class CategoryDelete(DeleteView):
    model = Category
    success_url = '/categorys/'
