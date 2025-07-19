from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from datetime import date, datetime
from django.utils.dateparse import parse_date
from .forms import RegistroForm, EventoForm
from .models import Evento
import re
import calendar
from collections import defaultdict

def index(request):
    eventos = Evento.objects.all().order_by('fecha')
    return render(request, 'index.html', {'eventos': eventos})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('index')
        else:
            messages.error(request, 'Hubo un error en el formulario. Por favor revisa los datos.')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {
        'register_form': form,
        'login_form': AuthenticationForm()
    })

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente.')
            return redirect('index')
        else:
            messages.error(request, 'Credenciales inválidas, intenta de nuevo.')
    else:
        form = AuthenticationForm()
    return render(request, 'registro.html', {
        'login_form': form,
        'register_form': RegistroForm()
    })

def es_superadmin(user):
    return user.is_superuser

@login_required
@user_passes_test(es_superadmin)
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento creado con éxito.')
            return redirect('index')
        else:
            messages.error(request, 'Corrige los errores en el formulario.')
    else:
        form = EventoForm()
    return render(request, 'crear_evento.html', {'form': form})

@login_required
@user_passes_test(es_superadmin)
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento actualizado correctamente.')
            return redirect('index')
        else:
            messages.error(request, 'Corrige los errores en el formulario.')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'editar_evento.html', {'form': form, 'evento': evento})

@login_required
@user_passes_test(es_superadmin)
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento eliminado exitosamente.')
        return redirect('index')
    return render(request, 'eliminar_evento.html', {'evento': evento})

@login_required
def carrito(request):
    return render(request, 'carrito.html')

def buscar_eventos(request):
    evento = escape(request.GET.get('evento', '').strip())
    artista = escape(request.GET.get('artista', '').strip())
    categoria = escape(request.GET.get('categoria', '').strip())
    fecha = escape(request.GET.get('fecha', '').strip())

    eventos = Evento.objects.all()

    if evento:
        eventos = eventos.filter(titulo__icontains=evento)
    if artista:
        eventos = eventos.filter(artista__icontains=artista)
    if categoria:
        eventos = eventos.filter(categoria__iexact=categoria)
    if fecha:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha):
            return HttpResponseBadRequest('Formato de fecha inválido.')
        eventos = eventos.filter(fecha=fecha)

    html = render_to_string('partials/lista_eventos.html', {'eventos': eventos, 'request': request})
    return JsonResponse({'html': html})

# -------------------------------
# VISTAS PARA EL CALENDARIO
# -------------------------------

def calendario(request):
    hoy = date.today()
    año = 2025

    # Filtrar eventos solo para el año 2025
    eventos = Evento.objects.filter(fecha__year=año).order_by('fecha')

    # Crear diccionario para eventos por (mes, día)
    eventos_por_dia = defaultdict(list)
    for evento in eventos:
        eventos_por_dia[(evento.fecha.month, evento.fecha.day)].append(evento)

    # Desde el mes actual si es 2025, si no mostrar desde enero
    mes_inicio = hoy.month if hoy.year == año else 1

    calendario_2025 = []
    cal = calendar.Calendar(firstweekday=0)  # Lunes como primer día

    for mes_num in range(mes_inicio, 13):
        nombre_mes = datetime(año, mes_num, 1).strftime('%B').capitalize()
        semanas = cal.monthdayscalendar(año, mes_num)
        calendario_2025.append({
            'mes': nombre_mes,
            'numero_mes': mes_num,
            'dias': semanas,
        })

    return render(request, 'calendario.html', {
        'hoy': hoy,
        'eventos': eventos,
        'calendario_2025': calendario_2025,
        'eventos_por_dia': dict(eventos_por_dia),  # para fácil acceso en la plantilla
    })

def api_eventos(request):
    start = parse_date(request.GET.get('start'))
    end = parse_date(request.GET.get('end'))

    eventos = Evento.objects.all()

    if start and end:
        eventos = eventos.filter(fecha__range=(start, end))

    data = []

    for evento in eventos:
        data.append({
            'title': evento.titulo,
            'start': str(evento.fecha),
            'description': evento.descripcion,
        })

    return JsonResponse(data, safe=False)
