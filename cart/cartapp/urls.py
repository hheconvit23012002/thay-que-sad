from django.urls import path, include
from . import views
urlpatterns = [
    path('addToCart/', views.addToCart),
    path('getCart/', views.getCart),
    path('deleteCart/', views.deleteCart),

]