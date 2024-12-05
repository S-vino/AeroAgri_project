from django.urls import path
from .import views

urlpatterns = [
    path('systemlogin/', views.systemlogin),
    path('system_logout/', views.system_logout),
    path('systemregister/', views.systemregister),
    path('system_home/', views.system_home),
    path('soil_report_data/', views.soil_report_data),
    path('process_sch/', views.process_sch),
    path('syscare_result/<str:client_id>/', views.syscare_result),
    path('sys_report/', views.sys_report)

]