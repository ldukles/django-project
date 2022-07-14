from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import LocationForm
from django.db.models import Q
import uuid
import boto3
from .models import Observation, Category, Photo

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'naturalist-avatar'

# HOME VIEW
def home(request):
  return render(request, 'home.html')

# ABOUT VIEW
def about(request):
  return render(request, 'about.html')


# MY OBSERVATION INDEX
@login_required
def observations_index(request):
    # observations = Observation.objects.all()
    observations = Observation.objects.filter(user=request.user)
    return render(request, 'observations/index.html', { 'observations': observations })

# ALL OBSERVATION INDEX
def allobservations(request):
    observations = Observation.objects.all()
    return render(request, 'allobservations/index.html', { 'observations': observations })

def allobservations_detail(request, observation_id):
    observation = Observation.objects.get(id=observation_id)
    return render(request, 'observations/detail.html', {'observation': observation})

# INDIVDUAL OBSERVATION DETAIL
@login_required
def observations_detail(request, observation_id):
    observation = Observation.objects.get(id=observation_id)
    location_form = LocationForm()
    categorys_observation_doesnt_have = Category.objects.exclude(id__in = observation.categorys.all().values_list('id'))
    return render(request, 'observations/detail.html', {
        'observation': observation, 'location_form': location_form,
        'categorys': categorys_observation_doesnt_have
  })

@login_required
def add_location(request, observation_id):
    form = LocationForm(request.POST)
    if form.is_valid():
        new_location = form.save(commit=False)
        new_location.observation_id = observation_id
        new_location.save()
    return redirect('detail', observation_id=observation_id)

# ASSOCIATING OBSERVATION WITH CATEGORY
@login_required
def assoc_category(request, observation_id, category_id):
  Observation.objects.get(id=observation_id).categorys.add(category_id)
  return redirect('detail', observation_id=observation_id)


# DELETING CATEGORY FROM ASSOCIATED OBSERVATION
@login_required
def assoc_category_delete(request, observation_id, category_id):
  Observation.objects.get(id=observation_id).categorys.remove(category_id)
  return redirect('detail', observation_id=observation_id)

# PHOTO UPLOAD
@login_required
def add_photo(request, observation_id):
    # photo-file will be the "name" attribute on the <input type="file">
    # attempt to collect the photo file data
    photo_file = request.FILES.get('photo-file', None)
    # use conditional logic to determine if file is present
    if photo_file:
    # if it's present, we will create a reference to the boto3 client
      s3 = boto3.client('s3')
      #Create unique ide for each photo file
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      #upload the photo phile to aws
      try:
      # if successful
        s3.upload_fileobj(photo_file, BUCKET, key)
        # take the exchanged url and save it to the database
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
          # 1. create photo instance with phot model and provide cat_id as foreign key value
        photo = Photo(url=url, observation_id=observation_id)
          # 2. save the photo instance to the database
        photo.save()
      # print an error message
      except Exception as error:
        print('An error occurred uploading file to S3')
    # redirect the user to the origin page
        return redirect('detail', observation_id=observation_id)
    return redirect('detail', observation_id=observation_id)
  # need a unique "key" for S3 / needs image file extension too 

def signup(request):
  error_message = ''
   # check if the request method is post
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    # create a new user because from was submitted
    # use the form data from the request to create a form/model instance from the model from
    form = UserCreationForm(request.POST)
    # validate the form to ensure it was complete
    if form.is_valid():
      # saving the user object to the database
      # This will add the user to the database
      user = form.save()
      # login the user (creates a session for the logged in user in the database)
      # This is how we log a user in via code
      login(request, user)
      # redirect user to cats index page
      return redirect('index')
    # if form not valid redirect user to signup page with an error message
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  # else the request is GET == the user clicked on the signup link
  # create a blank instance of the model form
  form = UserCreationForm()
  # provide that form instance to a registration template
  context = {'form': form, 'error_message': error_message}
  # render the template so the user can fill out the form
  return render(request, 'registration/signup.html', context)

class ObservationCreate(LoginRequiredMixin, CreateView):
    model = Observation
    fields = ['name', 'sciname', 'amount', 'description', 'details']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ObservationUpdate(LoginRequiredMixin, UpdateView):
  model = Observation
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['name', 'sciname', 'amount', 'description', 'details']

class ObservationDelete(LoginRequiredMixin, DeleteView):
  model = Observation
  success_url = '/observations/'

class CategoryList(LoginRequiredMixin, ListView):
  model = Category
  template_name = 'categorys/index.html'

class CategoryDetail(LoginRequiredMixin, DetailView):
  model = Category
  template_name = 'categorys/detail.html'

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['classification']


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['classification']


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = '/categorys/'

class SearchResultsView(LoginRequiredMixin, ListView):
    model = Observation
    template_name = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Observation.objects.filter(
            Q(name__icontains=query)
        )
        return object_list
