from django.urls import path, include
from . import views
urlpatterns = [
    path('comment/', views.comment),
    path('getListComment/',views.getListComment)
]