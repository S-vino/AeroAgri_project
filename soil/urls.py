from django.urls import path
from .import views

urlpatterns = [
    path('soilregister/', views.soilregister),
    path('soillogin/',views.soillogin),
    path('soil_logout/',views.soil_logout),
    path('soil_home/', views.soil_home),
    path('s_aero_report/', views.s_aero_report),
    path('aero_process_data/', views.aero_process_data),
    path('compare_plant_types/<str:client_id>/', views.compare_plant_types),
    path('soil_result/', views.soil_result),

]