from django.urls import path
from .import views

urlpatterns = [
    path('admins_login/', views.admins_login),
    path('admins_logout/', views.admins_logout),
    path('admins_home/', views.admins_home),
    path('client_details/', views.client_details),
    path('approve/<int:id>/', views.approve),
    path('reject/<int:id>/', views.reject),
    path('am_details/', views.am_details),
    path('aero_approve/<int:id>/', views.aero_approve),
    path('aero_reject/<int:id>/', views.aero_reject),
    path('soil_details/', views.soil_details),
    path('soil_approve/<int:id>/', views.soil_approve),
    path('soil_reject/<int:id>/', views.soil_reject),
    path('system_details/', views.system_details),
    path('system_approve/<int:id>/', views.system_approve),
    path('system_reject/<int:id>/', views.system_reject),
    path('aero_report/', views.aero_report),
    path('soil_report/', views.soil_report),
    path('invoicehome/', views.invoicehome),
    path('invoice/<int:id>/', views.invoice),

    path('system_report/', views.system_report),
    path('payslip/', views.payslip)

]