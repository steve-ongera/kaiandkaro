# cars/urls.py (app urls)
from django.urls import path
from . import views


urlpatterns = [
    # Main pages
    path('', views.home_view, name='home'),
    path('cars/', views.car_list_view, name='car_list'),
    path('cars/<slug:slug>/', views.car_detail_view, name='car_detail'),
    
    # Static pages
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    # AJAX endpoints
    path('api/models-by-brand/', views.get_models_by_brand, name='models_by_brand'),
    
    # Alternative class-based view URLs (if you prefer to use them)
    # path('cars/', views.CarListView.as_view(), name='car_list_cbv'),
    # path('cars/<slug:slug>/', views.CarDetailView.as_view(), name='car_detail_cbv'),
]
