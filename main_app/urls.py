
from django.urls import path
from . import views
from .views import SearchResultsView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('observations/', views.observations_index, name='index'),
    # path('allobservations/', views.allobservations_index, name='allobservations'),
    path('observations/<int:observation_id>/', views.observations_detail, name='detail'),
    path('observations/create/', views.ObservationCreate.as_view(), name='observations_create'),
    path('observations/<int:pk>/update/', views.ObservationUpdate.as_view(), name='observations_update'),
    path('observations/<int:pk>/delete/', views.ObservationDelete.as_view(), name='observations_delete'),
    path('observations/<int:observation_id>/add_location/', views.add_location, name='add_location'),
    path('observations/<int:observation_id>/assoc_category/<int:category_id>/', views.assoc_category, name='assoc_category'),
    path('observations/<int:observation_id>/assoc_category/<int:category_id>/delete', views.assoc_category_delete, name='assoc_category_delete'),
    path('categorys/', views.CategoryList.as_view(), name='categorys_index'),
    path('categorys/<int:pk>/', views.CategoryDetail.as_view(), name='categorys_detail'),
    path('categorys/create/', views.CategoryCreate.as_view(), name='categorys_create'),
    path('categorys/<int:pk>/update/', views.CategoryUpdate.as_view(), name='categorys_update'),
    path('categorys/<int:pk>/delete/', views.CategoryDelete.as_view(), name='categorys_delete'),
    path('observations/<int:observation_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
    path("search/", SearchResultsView.as_view(), name="search_results"),
]