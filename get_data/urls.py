from django.urls import path

from . import views


urlpatterns = [
   path('', views.index),
   path('celery/', views.test, name='test'),
   path('add/', views.add_to_db, name='add_to_db'),
   path('manualy/', views.add_manualy, name='add_manualy'),
   
]