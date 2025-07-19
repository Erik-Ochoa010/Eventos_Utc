from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('buscar-eventos/', views.buscar_eventos, name='buscar_eventos'),
    path('calendario/', views.calendario, name='calendario'),
    path('api/eventos/', views.api_eventos, name='api_eventos'),
    path('crear-evento/', views.crear_evento, name='crear_evento'),
    path('editar/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eliminar/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('carrito/', views.carrito, name='carrito'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]
