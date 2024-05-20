from django.urls import path, include
from . import views

urlpatterns = [
    path('getListBook/', views.getListBook),
    path('addBook/', views.addBook),
    path('update_number_product/', views.updateNumber),
    path('check_number_product/', views.checkNumber),
    path('get_detail_product/<int:id>/', views.getDetailProduct),
]