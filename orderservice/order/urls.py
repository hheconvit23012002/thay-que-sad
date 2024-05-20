from django.urls import path, include
from . import views
urlpatterns = [
    path('checkout/', views.checkout),
    path('getListOrder/', views.getListOrder),
    path('getListAllOrder/', views.getListAllOrder),
    path('updateStatusPaid/', views.updateStatusPaid),
]