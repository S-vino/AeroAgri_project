from django.urls import path
from .import views

urlpatterns = [
    path('aeroregister/', views.aeroregister),
    path('aerologin/', views.aerologin),
    path('aero_logout/',views.aero_logout),
    path('aero_home/', views.aero_home),
    path('requirement/', views.requirement),
    path('process/', views.process),
    path('process_aero/<str:client_id>/',views.process_aero),
    path('view_report/',views.view_report),


]