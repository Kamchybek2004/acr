from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate
from .models import User
import re


class RegisterForm(UserCreationForm):
    last_name = forms.CharField(
        label='Фамилия', 
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Абдыжалилов"})
        )

    first_name = forms.CharField(
        label='Аты', 
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Камчыбек"})
    )

    email = forms.EmailField(
        label='Электрондук почта', 
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "example@gmail.com"})
    )

    password1 = forms.CharField(
        label="Сыр сөз",
        widget=forms.PasswordInput(attrs={"id": "password1", "placeholder": ""})
    )

    password2 = forms.CharField(
        label="Сыр сөздү тастыктаңыз",
        widget=forms.PasswordInput(attrs={"id": "password2", "placeholder": ""})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Бул электрондук почта менен катталган колдонуучу буга чейин бар.")
        return email

    # ==================
    # Проверка пароля
    # ==================


    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise forms.ValidationError("Сыр сөз кеминде 8 белгиден(символ) турушу керек.")

        if not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError("Сыр сөз кеминде бир латын тамгасын камтышы керек.")

        if not re.search(r'\d', password):
            raise forms.ValidationError("Сыр сөз кеминде бир санды камтышы керек.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Сыр сөз кеминде бир атайын белгини(символ) камтышы керек !@#$%^&*(),.?}{:|<>.")

        return password 

    def clean_password2(self):
        password = self.cleaned_data.get('password2')

        if len(password) < 8:
            raise forms.ValidationError("Сыр сөз кеминде 8 белгиден(символ) турушу керек.")

        if not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError("Сыр сөз кеминде бир латын тамгасын камтышы керек.")

        if not re.search(r'\d', password):
            raise forms.ValidationError("Сыр сөз кеминде бир санды камтышы керек.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Сыр сөз кеминде бир атайын белгини(символ) камтышы керек !@#$%^&*(),.?}{:|<>.")

        return password


    # Проверка совпадение паролей

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Пароли не совпадают")

        return cleaned_data


class LoginForm(forms.Form):
    name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={"placeholder": "Введите своё имя"})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={"placeholder": "example@gmail.com"})
    )

    password = forms.CharField(
        label='Сыр сөз',
        widget=forms.PasswordInput(attrs={"id": "password", "placeholder": ""})
    )

    def clean(self):
        cleaned_data = super().clean()
        name=cleaned_data.get('name')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and name and password:
            try:
                user_obj = User.objects.get(email=email, first_name=name)
            except User.DoesNotExist:
                raise forms.ValidationError("Аккаунт с таким email или с именем не существует")

            if not user_obj.is_active:
                raise forms.ValidationError("Аккаунт отключён")

            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Неверный email или пароль")

            cleaned_data['user'] = user

        return cleaned_data


# ===================
#  Сброс пароля
# ===================

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input-wrapper',
            'placeholder': 'Введите ваш email'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-wrapper',
            'placeholder': 'Новый пароль',
            'id': 'id_new_password1'
        })
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-wrapper',
            'placeholder': 'Подтвердите пароль',
            'id': 'id_new_password2'
        })
    )