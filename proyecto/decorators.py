from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Progreso

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
        if group == 'estudiante':
            return redirect('estudiante')
        if group == 'administrador':
            return view_func(request, *args, **kwargs )
    return wrapper_function

def permitir_paso1():
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            estudiante = request.user.datosestudiante
            if Progreso.objects.filter(usuario=estudiante).exists():
                progreso = Progreso.objects.get(usuario=estudiante).nivel
            else:
                progreso = 1
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
            if Progreso.objects.filter(usuario=estudiante).exists():
                progreso = Progreso.objects.get(usuario=estudiante).nivel
            else:
                progreso = 1
            if progreso >= 19:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No se concluyo el paso 1, habilitar con 19 % de progreso')
        return wrapper_function
    return decorator

def permitir_paso3():
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            estudiante = request.user.datosestudiante
            if Progreso.objects.filter(usuario=estudiante).exists():
                progreso = Progreso.objects.get(usuario=estudiante).nivel
            else:
                progreso = 1
            if progreso >= 25:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No se concluyo el paso 2, habilitar con 19 % de progreso')
        return wrapper_function
    return decorator

def permitir_paso4():
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            estudiante = request.user.datosestudiante
            if Progreso.objects.filter(usuario=estudiante).exists():
                progreso = Progreso.objects.get(usuario=estudiante).nivel
            else:
                progreso = 1
            if progreso >= 31:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No se concluyo el paso 3, habilitar con 31 % de progreso')
        return wrapper_function
    return decorator

def permitir_paso5():
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            estudiante = request.user.datosestudiante
            if Progreso.objects.filter(usuario=estudiante).exists():
                progreso = Progreso.objects.get(usuario=estudiante).nivel
            else:
                progreso = 1
            if progreso >= 69:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No se concluyo el paso 4, habilitar con 69 % de progreso')
        return wrapper_function
    return decorator

def permitir_paso6():
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            estudiante = request.user.datosestudiante
            if Progreso.objects.filter(usuario=estudiante).exists():
                progreso = Progreso.objects.get(usuario=estudiante).nivel
            else:
                progreso = 1
            if progreso >= 81:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No se concluyo el paso 5, habilitar con 81 % de progreso')
        return wrapper_function
    return decorator
