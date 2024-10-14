from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index.html'),
    path('productos/', views.lista_productos  , name='lista_productos'),
    path('contacto/', views.contacto_cliente  , name='contacto_cliente'),
    path('guia_y_tutorial/', views.guia_tutorial, name='guia_tutorial')
]