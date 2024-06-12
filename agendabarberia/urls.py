from django.urls import path
from .views import barberias, registrar_barberia, editar_barberia, perfil_barberia, eliminar_barberia, registrar_usuario, iniciar_sesion, cerrarSesion, reservas, error, solicitar_cita, eliminar_cita, editarUsuario, perfilUsuario

urlpatterns = [
    path('', iniciar_sesion, name='iniciar-sesion'), 
    path('cerrar-sesion', cerrarSesion, name="cerrar-sesion"), 
    path('registrar-usuario/', registrar_usuario, name='registrar-usuario'),
    path('editar-usuario/<int:usuario_id>/', editarUsuario, name="editar-usuario"),
    path('perfil-usuario/<int:usuario_id>', perfilUsuario, name="perfil-usuario"),
    path('barberias/', barberias, name='barberias'),
    path('registrar-barberia/', registrar_barberia, name='registrar-barberia'),
    path('editar-barberia/<int:barberia_id>/', editar_barberia, name='editar-barberia'),
    path('perfil-barberia/<int:barberia_id>/', perfil_barberia, name='perfil-barberia'),
    path('eliminar-barberia/<int:barberia_id>/', eliminar_barberia, name='eliminar-barberia'),
    path('reservas/', reservas, name='reservas'),
    path('barberia/<int:barberia_id>/solicitar_cita/', solicitar_cita, name='solicitar-cita'),
    path('reservas/<int:cita_id>/eliminar_cita/', eliminar_cita, name='eliminar-cita'),
    path('error/',error, name='error')

]