from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Session, Film
import re


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'})
    )
    email = forms.EmailField(required=True)

    # Убрали поле captcha отсюда

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'password1', 'password2']

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[а-яА-ЯёЁ\s]+$', full_name):
            raise forms.ValidationError('ФИО должно содержать только кириллические символы')
        return full_name

    def clean_password1(self):
        password = self.cleaned_data['password1']
        if len(password) < 6:
            raise forms.ValidationError('Пароль должен содержать минимум 6 символов')
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
            raise forms.ValidationError('Пароль должен содержать символы верхнего и нижнего регистра')
        return password


# Остальные формы без изменений
class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['film', 'datetime', 'price', 'seats_available']
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['title', 'description', 'duration', 'genre']