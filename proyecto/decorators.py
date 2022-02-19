from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Progreso
from actividades.funciones import *

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No estas autorizado para esta pagina')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'docente':
            return redirect('docente')
        if group == 'tutor':
            return redirect('tutor')
        if group == 'tribunal':
            return redirect('tribunal')
        if group == 'estudiante':
            return redirect('estudiante')
        if group == 'director':
            return redirect('director')
        if group == 'solicitud':
            return redirect('solicitud')
        if group == 'administrador':
            return view_func(request, *args, **kwargs )
    return wrapper_function

def permitir_con(pasos=[]):
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            pp = pasosRealizados(request.user.datosestudiante)
            c_pp = set(pp)
            c_pasos = set(pasos)
            print(c_pp, c_pasos)
            if c_pp <= c_pasos:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('error')
        return wrapper_function
    return decorator

def permitir_paso1():
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            estudiante = request.user.datosestudiante
            # if Progreso.objects.filter(usuario=estudiante).exists():
                # progreso = Progreso.objects.get(usuario=estudiante).nivel
            # else:
                # progreso = 1
            progreso = progress(estudiante)
            if progreso >= 1:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No se concluyo el anterior paso')
        return wrapper_function
    return decorator

def permitir_paso2():
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            estudiante = request.user.datosestudiante
            # if Progreso.objects.filter(usuario=estudiante).exists():
                # progreso = Progreso.objects.get(usuario=estudiante).nivel
            # else:
                # progreso = 1
            progreso = progress(estudiante)
            if progreso >= 14:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No se concluyo el paso 1, habilitar con 14 % de progreso')
        return wrapper_function
    return decorator

def permitir_paso3():
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            estudiante = request.user.datosestudiante
            # if Progreso.objects.filter(usuario=estudiante).exists():
                # progreso = Progreso.objects.get(usuario=estudiante).nivel
            # else:
                # progreso = 1
            progreso = progress(estudiante)
            if progreso >= 21:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No se concluyo el paso 2, habilitar con 21 % de progreso')
        return wrapper_function
    return decorator

def permitir_paso4():
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            estudiante = request.user.datosestudiante
            # if Progreso.objects.filter(usuario=estudiante).exists():
                # progreso = Progreso.objects.get(usuario=estudiante).nivel
            # else:
                # progreso = 1
            progreso = progress(estudiante)
            if progreso >= 35:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No se concluyo el paso 3, habilitar con 35 % de progreso')
        return wrapper_function
    return decorator

def permitir_paso5():
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            estudiante = request.user.datosestudiante
            # if Progreso.objects.filter(usuario=estudiante).exists():
                # progreso = Progreso.objects.get(usuario=estudiante).nivel
            # else:
                # progreso = 1
            progreso = progress(estudiante)
            if progreso >= 64:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No se concluyo el paso 4, habilitar con 64 % de progreso')
        return wrapper_function
    return decorator

def permitir_paso6():
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            estudiante = request.user.datosestudiante
            # if Progreso.objects.filter(usuario=estudiante).exists():
                # progreso = Progreso.objects.get(usuario=estudiante).nivel
            # else:
                # progreso = 1
            progreso = progress(estudiante)
            if progreso >= 86:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No se concluyo el paso 5, habilitar con 86 % de progreso')
        return wrapper_function
    return decorator
