# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Major, Profile, License, Order, Module
from  django.http import Http404
from django.db.models import Prefetch

# Главная страница
def index(request):
    majors = Major.objects.prefetch_related('profiles').all()
    return render(request, "core/index.html", {'majors': majors})

# Таблица образовательных программ
def edu_program(request):
    majors = Major.objects.prefetch_related('profiles').all()
    return render(request, "core/edu_program.html", {'majors': majors})

# Профиль образования 
def profile_detail(request, slug):
    letter = request.GET.get('letter') # буква

    modules_qs = Module.objects.all().order_by('name')

    if letter:
        modules_qs = modules_qs.filter(name__istartswith=letter)

    profile = get_object_or_404(
        Profile.objects.prefetch_related(
            'documents',
            'competence_passports',
            Prefetch('modules', queryset=modules_qs),
        ),
        slug=slug
    )
    
    return render(request, "core/profile_detail.html", {
        'profile': profile,
        'modules': profile.modules.all(),
        'selected_letter': letter,
        })

# Нормативные документы
def document(request):  
    orders = Order.objects.all()
    categories = {
        'kr_laws': orders.filter(category='kr_laws'),
        'gov_resolution': orders.filter(category='gov_resolution'),
        'ministry_orders': orders.filter(category='ministry_orders'),
        'nsu_orders': orders.filter(category='nsu_orders'),
        'gos': oreders.filter(category='gos'),
        'smk1': orders.filter(category='smk1'),
        'smk2': orders.filter(category='smk2'),
        'smk3': orders.filter(category='smk3'),
        'smk4': orders.filter(category='smk4'),
        'smk5': orders.filter(category='smk5'),
    }
    return render(request, "core/document.html", {'categories': categories})

# Лицензии
def license(request):
    licenses = License.objects.all()
    return render(request, "core/license.html", {'licenses': licenses})

# Войти
def login(request): 
    return render(request, "core/login.html")

# Регистрация 
def register(request):
    return render(request, "core/register.html")

def profile_index(request):
    raise Http404('Page not found') 