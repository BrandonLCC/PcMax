from django import forms
from .models import Contacto
from .models import CarritoProducto
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactoForm(forms.ModelForm):
  
    class Meta:
        
        model = Contacto
       
        fields = ['nombre', 'email', 'mensaje']
      
        widgets = {
           
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
         
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
      
            'mensaje': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CarritoProductoForm(forms.ModelForm):
    class Meta:
        model = CarritoProducto
        fields = ['producto', 'cantidad']

class InicioSesion(forms.ModelForm):
    class Meta:
        model = Usuario  # MODEL ES EL MODELO QUE DEFINIMOS EN LA PAGINA MODEL DONDE OBTENEMOS LOS ATRIBUTOS DE USUARIO
        fields = ['nombre_usuario', 'contraseña_usuario']
        widgets = {
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'contraseña_usuario': forms.PasswordInput(attrs={'class': 'form-control'}),  # Asegúrate de que el campo de contraseña sea seguro
        }

class RegistroUsuarioForm(UserCreationForm):
   email = forms.EmailField()
   password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput)
   password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)

   class Meta: 
    model = User
    fields = ['username','email','password1','password2']
    help_texts = {k:"" for k in fields }

class CantidadProductoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, initial=1, label='Cantidad')



class CantidadProductoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')