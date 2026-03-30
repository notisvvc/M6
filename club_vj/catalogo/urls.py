from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('videojuegos', videojuegos, name='videojuegos'),
    path('videojuego/<int:id>/', videojuego_detalle, name='videojuego' ),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),

]