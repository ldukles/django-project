
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('observations/', views.observations_index, name='index'),
    path('observations/<int:observation_id>/', views.observations_detail, name='detail'),
]