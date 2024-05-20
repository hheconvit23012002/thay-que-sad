from django.urls import path
from . import views 

urlpatterns = [ 
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.getUserProfile, name='get-user-profile'),
    path('register/', views.registerUser, name='resgister'),
    path('updateUser/', views.updateUser, name='updateUser'),
]