from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Observation
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
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

# PHOTO UPLOAD
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
        photo = Photo(url=url, cat_id=observation_id)
          # 2. save the photo instance to the database
        photo.save()
      # print an error message
      except Exception as error:
        print('An error occurred uploading file to S3')
    # redirect the user to the origin page
        return redirect('detail', observation_id=observation_id)
    return redirect('detail', observation_id=observation_id)
  # need a unique "key" for S3 / needs image file extension too 

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
