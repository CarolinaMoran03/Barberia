from django.shortcuts import render, redirect, get_object_or_404
from .forms import BarberiaForm, CustomUserCreationForm, EditUserForm
from .models import Barberia, Cita
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.translation import activate
from django.utils import timezone
from datetime import timedelta
import random
from django.conf import settings

# Enviar Correo dependencias
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Barberia acciones


@login_required
def barberias(request):
    barberias = Barberia.objects.all()
    user = request.user 
    citas = Cita.objects.filter(usuario=user)
    print(user.email)

    hoy = timezone.now()

    for cita in citas:
        fecha_cita = cita.fecha
        falta_un_dia = False
        if hoy.date() == (fecha_cita - timedelta(days=1)).date() and hoy.hour == fecha_cita.hour:
            falta_un_dia = True
            if user.email:  # Verifica que el usuario tenga un correo válido
                email = user.email
                enviarCorreosAutomaticos(email)
           

    notificaciones_citas = citas.count()
    return render(request, 'barberias.html', {'barberias': barberias, 'user':user, 'notificaciones':notificaciones_citas})




@login_required
def registrar_barberia(request):
    if request.method == 'POST':
        form = BarberiaForm(request.POST, request.FILES)
        if form.is_valid():
            barberia = form.save(commit=False)
            barberia.usuario = request.user  # Asigna el usuario actual
            barberia.save()
            return redirect('barberias')
    else:
        form = BarberiaForm()
    return render(request, 'registrar-barberia.html', {'form': form})



@login_required
def perfil_barberia(request, barberia_id):
    barberia = get_object_or_404(Barberia, pk=barberia_id)
    user = request.user
    citas = Cita.objects.filter(usuario=user, barberia=barberia)
    hoy = timezone.now()
    hace_una_semana = hoy - timedelta(days=7)
    citas_en_ultima_semana = Cita.citas_en_ultima_semana(user)
    notificaciones_citas = citas.count()


    total_citas_en_barberia = citas.count()
    mostrar_cupon = total_citas_en_barberia >= 9 #gestiona cuantas vecces va a la barberia
    

    numeroAleatorio = random.randint(1, 400)

    barberCodeCupon = ([f'code:{user}12/{hoy}/{numeroAleatorio}',f'code:{user}34/{hoy}/{numeroAleatorio}',f'code:{user}56/{hoy}/{numeroAleatorio}', f'code:{user}78/{hoy}/{numeroAleatorio}'])
    print(barberCodeCupon)

    cuponAleatorio = random.choice(barberCodeCupon)

    return render(request, 'perfil-barberia.html', {
        'user': user,
        'barberia': barberia, 
        'notificaciones': notificaciones_citas, 
        'cupon': mostrar_cupon,
        'cuponCode': cuponAleatorio
        
    })



@login_required
def editar_barberia(request, barberia_id):
    barberia = get_object_or_404(Barberia, pk=barberia_id)

    # Verifica si el usuario actual es el creador de la barbería
    if request.user != barberia.usuario:
        # Puedes redirigir a alguna página o mostrar un mensaje de error
        return render(request, 'error.html', {'message': 'No tienes permisos para editar esta barbería.'})

    if request.method == 'POST':
        form = BarberiaForm(request.POST, request.FILES, instance=barberia)
        if form.is_valid():
            form.save()
            return redirect('perfil-barberia', barberia_id=barberia_id)
    else:
        form = BarberiaForm(instance=barberia)

    return render(request, 'editar_barberia.html', {'form': form, 'barberia': barberia})



@login_required
def eliminar_barberia(request, barberia_id):
    barberia = get_object_or_404(Barberia, pk=barberia_id)

    # Verifica si el usuario actual es el propietario de la barbería
    if request.user == barberia.usuario:
        barberia.delete()
        return redirect('barberias')
    else:
       
        return HttpResponseForbidden("No tienes permisos para eliminar esta barbería.")



# Inicio de sesion

def iniciar_sesion(request):
    activate('es')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}')
                return redirect('barberias')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    
    form = AuthenticationForm()
    return render(request,'iniciar-sesion.html', {"form":form})


def cerrarSesion(request):
    logout(request)
    return redirect('iniciar-sesion')


def registrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('iniciar-sesion')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registrar-usuario.html', {'form': form})


def editarUsuario(request, usuario_id):
    user = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('perfil-usuario', usuario_id=user.id)  # redirigir a una vista de detalles del usuario
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'editarPerfilUsuario.html', {'form': form})


def perfilUsuario(request, usuario_id):
    user = request.user
    email = user.email.lower()
    return render(request, 'perfilUsuario.html', {
        'user': user,
        'email': email
    })

#reservas

def reservas(request):
    current_user = request.user
    citas = Cita.objects.filter(usuario=current_user)
    notificaciones_citas = citas.count()  
  

   

    
    return render(request, 'reservas.html', {
        'user': current_user,
        'citas': citas, 
        'notificaciones': notificaciones_citas,
    
        
        
    })

# def reservas(request):
#     return render(request, 'reservas.html')


@login_required
def solicitar_cita(request, barberia_id):
    barberia = Barberia.objects.get(id=barberia_id)
    current_user = request.user

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        plan = request.POST.get('plan')
        print(plan)
        cita = Cita.objects.create(usuario=current_user, barberia=barberia, fecha=fecha, plan=plan)
        return redirect('reservas')


    # Realizar la lógica para crear la cita con la información disponible
    # peticion = Cita.objects.create(usuario=current_user, barberia=barberia)

    # Redirigir a la página que muestra las citas de esta barbería
    citas = Cita.objects.filter(barberia=barberia)
    return render(request, 'reservas.html', {'barberia': barberia, 'citas': citas})



#eliminar cita
def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)
    cita.delete()
    return redirect('reservas')

    


def error(request):
    return render(request, 'error.html')





def enviarCorreosAutomaticos(dest):
    load_dotenv()

    remitente = os.getenv('USER')
    print('remi', remitente)
    destinatario = dest
    asunto = 'Tienes una cita pendiente'
    print(destinatario)


    msg = MIMEMultipart()
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = destinatario

    template_path = os.path.join(settings.BASE_DIR, 'agendabarberia', 'templates', 'sendEmail.html')

    with open(template_path, 'r') as archivo:
        html = archivo.read()

    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PASSWORD'))

    server.sendmail(remitente, destinatario, msg.as_string())


    server.quit()