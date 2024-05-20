from django.urls import path, include
from . import views
urlpatterns = [
    path('shiperReceiver/', views.shiperReceiver),
    path('updateShip/', views.updateShip),
    path('infoShip/', views.infoShip),


]