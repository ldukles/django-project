
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('observations/', views.observations_index, name='index'),
    path('observations/<int:observation_id>/', views.observations_detail, name='detail'),
    path('observations/create/', views.ObservationCreate.as_view(), name='observations_create'),
    path('observations/<int:pk>/update/', views.ObservationUpdate.as_view(), name='observations_update'),
    path('observations/<int:pk>/delete/', views.ObservationDelete.as_view(), name='observations_delete'),

]