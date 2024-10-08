from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index.html'),
    path('productos/', views.lista_productos  , name='lista_productos'),

]