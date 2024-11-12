from django import forms
from .models import Contacto
from .models import CarritoProducto
from .models import Usuario

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre','email','mensaje']
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

class RegistroUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'gmail_usuario','contraseña_usuario']
        widgets = {
                'nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
                'gmail_usuario': forms.EmailInput(attrs={'class': 'form-control'}),
                'contraseña_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            }

class CantidadProductoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, initial=1, label='Cantidad')



class CantidadProductoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')