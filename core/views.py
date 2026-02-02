# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Major, Profile, License, Order
from  django.http import Http404

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
    profile = get_object_or_404(
        Profile.objects.prefetch_related(
            'documents',
            'modules',
            'competence_passports'
        ),
        slug=slug
    )
    
    return render(request, "core/profile_detail.html", {'profile': profile})

# Нормативные документы
def document(request):  
    orders = Order.objects.all()
    categories = {
        'kr_laws': orders.filter(category='kr_laws'),
        'gov_resolution': orders.filter(category='gov_resolution'),
        'ministry_orders': orders.filter(category='ministry_orders'),
        'nsu_orders': orders.filter(category='nsu_orders'),
        'smk1': orders.filter(category='smk1'),
        'smk2': orders.filter(category='smk2'),
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