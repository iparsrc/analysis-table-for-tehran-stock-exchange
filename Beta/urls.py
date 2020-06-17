from django.urls import path
from . import views


urlpatterns = [
    path('', views.beta),
    path('update/', views.dataUpdate),
    path('data/csv/', views.sendCsvData),
]