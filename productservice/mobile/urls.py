from django.urls import path, include
from . import views
urlpatterns = [
    path('getListMobile/', views.getListMobile),
    path('addMobile/', views.addMobile),
]