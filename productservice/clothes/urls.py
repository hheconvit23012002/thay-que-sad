from django.urls import path, include
from . import views
urlpatterns = [
    path('getListClothes/', views.getListClothes),
    path('addClothes/', views.addClothes),
]