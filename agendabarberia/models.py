from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


ciudad = (('guayaquil', 'guayaquil'), ('santa-elena', 'santa-elena'), ('milagro', 'milagro'), ('duran', 'duran'))
planes = (('Básico', 'Básico'), ('Deluxe', 'Deluxe'), ('VIP', 'VIP'))
# Create your models here.
class Barberia(models.Model):
    imagen = models.ImageField(upload_to='barberia_images/')  # Guarda las imágenes en la carpeta 'barberia_images/'
    titulo = models.CharField(max_length=100)
    maps = models.CharField(max_length=100, default='https://maps.app.goo.gl/4Z6tBPcvjYrki5nK8')
    insta = models.CharField(max_length=100, default='https://www.instagram.com/')
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=200, choices=ciudad, default='*')
    numero_contacto = models.CharField(max_length=15)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.titulo
    

# type_user =  (('Barbero', 'barbero'), ('Cliente', 'cliente'))

# class Usuario(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     tipo_usuario = models.CharField(max_length=10, choices=type_user, default="Cliente")

#     def __str__(self) -> str:
#         return self.username
    

class Cita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    barberia = models.ForeignKey(Barberia, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)  # Asegúrate de tener este campo
    plan = models.CharField(max_length=10, choices=planes, default='Básico')

    @staticmethod
    def citas_en_ultima_semana(usuario):
        hoy = timezone.now()
        hace_una_semana = hoy - timedelta(days=7)
        return Cita.objects.filter(usuario=usuario, fecha__range=(hace_una_semana, hoy)).count()


    def __str__(self):
        return self.usuario
    


