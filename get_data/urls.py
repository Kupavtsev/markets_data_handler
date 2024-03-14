from django.urls import path

from . import views


urlpatterns = [
   #  main
   path('', views.index),
   path('celery/', views.test, name='test'),
   # requests
   path('add/', views.add_to_db, name='add_to_db'),
   path('add_2h/', views.two_hours_to_db, name='two_hours_to_db'),
   path('atrtotal/', views.atr, name='atr'),
   # logic
   path('mp2h/', views.calc_2h_mp, name='calc_2h_mp'),
   # api
   path('api/ohlc_atr', views.ohlc_atr, name='ohlc_atr')
]