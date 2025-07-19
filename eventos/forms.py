from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Evento
from django.core.exceptions import ValidationError
import re
import os

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError("El nombre de usuario contiene caracteres inválidos.")
        return username

class EventoForm(forms.ModelForm):

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        if '<script>' in titulo.lower():
            raise ValidationError("Título contiene código no permitido.")
        return titulo

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        # Aquí podrías agregar sanitización si usas campos html, pero si es texto plano,
        # Django automáticamente escapa, así que está bien.
        return descripcion

    def clean_artista(self):
        artista = self.cleaned_data['artista']
        if '<script>' in artista.lower():
            raise ValidationError("Nombre de artista contiene código no permitido.")
        return artista

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            ext = os.path.splitext(imagen.name)[1].lower()
            allowed = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            if ext not in allowed:
                raise ValidationError("Solo se permiten imágenes (.jpg, .jpeg, .png, .gif, .webp).")
            if imagen.size > 5 * 1024 * 1024:
                raise ValidationError("La imagen no puede pesar más de 5MB.")
        return imagen

    class Meta:
        model = Evento
        fields = ['titulo', 'artista', 'hora', 'descripcion', 'fecha', 'categoria', 'imagen']
