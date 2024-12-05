from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('login/', views.Clientlogin),
    path('register/', views.register),
    path('client_logout/', views.client_logout),
    path('client_home/',views.client_home),
    path('client_upload/', views.client_upload),
    path('product_status/', views.product_status),
    path('id/', views.id),
    path('status/', views.status),
    path('process_payment/<str:client_id>/', views.process_payment),
    path('client/', views.client),
    path('final_report/<str:client_id>/', views.final_report),
    path('read/<str:client_id>/', views.read),


]
urlpatterns += static(settings.MEDIA_URL,document_root=settings
                      .MEDIA_ROOT)
