# core/urls.py
from django.views.defaults import page_not_found
from django.http import HttpRequest
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("edu_program/", views.edu_program, name="edu_program"),
    path("profile/<slug:slug>/", views.profile_detail, name="profile_detail"),
    path("document/", views.document, name="document"),
    path("license/", views.license, name="license"),
    path("login/", views.login, name="login"),
    path("registration/", views.register, name="register"),
    path('profile/', views.profile_index)
] 