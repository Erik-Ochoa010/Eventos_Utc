from django.db import models

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()  # Solo la fecha
    hora = models.CharField(max_length=100)  # Hora en texto libre
    categoria = models.CharField(max_length=50)
    artista = models.CharField(max_length=100)  # Nombre del artista
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)

    def __str__(self):
        return self.titulo
