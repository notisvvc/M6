from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from .models import *

def index(request):
    context = {}
    return render(request, 'index.html', context)

@login_required
def videojuegos(request):
    vj = VideoJuego.objects.select_related('plataforma','genero')
    ano_actual = date.today().year

    context = { 'videojuegos': vj , 'ano_actual': ano_actual }
    
    return render(request, 'videojuegos.html', context)

@login_required
def videojuego_detalle(request, id):
    print(id)
    vj = VideoJuego.objects.select_related('plataforma','genero').filter(id=id).first()
    print(vj)

    context = { "detalle_vj": vj}
    return render(request, 'videojuego_detalle.html', context)


class RegisterView(View):
    def get(self, request):
        return render(request, 'registration/register.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        rut = request.POST.get('rut')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect(reverse('register'))  
        user = User.objects.create_user(username=email, email=email, password=password1, first_name=first_name, last_name=last_name)
        #user.is_active = False
        UserProfile.objects.create(user=user, rut=rut, direccion=direccion, telefono=telefono, vip=False )
        user.save()
        user = authenticate(username=email, password=password1)
        if user is not None:
            login(request, user)
        messages.success(request, 'Usuario creado exitosamente')
        return redirect('index')
    
class CustomLoginView(SuccessMessageMixin, LoginView):
    success_message = "Sesion Iniciada Exitosamente"
    template_name = 'registration/login.html'  
    redirect_authenticated_user = True
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.WARNING, "Sesion Cerrada Exitosamente")
        return response