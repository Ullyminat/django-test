from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .models import Session, Booking, Film, CustomUser
from .forms import RegisterForm, SessionForm, FilmForm
import random
import string

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        # Проверка капчи
        user_captcha = request.POST.get('captcha', '')
        session_captcha = request.session.get('captcha_text', '')

        if user_captcha.upper() != session_captcha:
            form.add_error('captcha', 'Неверная капча')

        if form.is_valid() and user_captcha.upper() == session_captcha:
            user = form.save()
            login(request, user)
            if user.username == 'admin':
                return redirect('admin_panel')
            return redirect('sessions_list')
    else:
        form = RegisterForm()
        # Генерируем новую капчу для сессии
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        request.session['captcha_text'] = captcha_text

    return render(request, 'register.html', {
        'form': form,
        'captcha_text': request.session.get('captcha_text', '')
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if username == 'admin':
                return redirect('admin_panel')
            return redirect('sessions_list')
        else:
            return render(request, 'login.html', {'error': 'Неверные учетные данные'})
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def sessions_list(request):
    sessions = Session.objects.all().order_by('datetime')

    search_query = request.GET.get('search', '')
    if search_query:
        sessions = sessions.filter(film__title__icontains=search_query)

    paginator = Paginator(sessions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sessions_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


@login_required
def book_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    if request.method == 'POST':
        if session.seats_available > 0:
            Booking.objects.create(
                user=request.user,
                session=session,
                tickets_count=1
            )
            session.seats_available -= 1
            session.save()
            return redirect('profile')
    return render(request, 'book_session.html', {'session': session})


@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'profile.html', {'bookings': bookings})


def is_admin(user):
    return user.username == 'admin'


@user_passes_test(is_admin)
@login_required
def admin_panel(request):
    return render(request, 'admin_panel.html')


@user_passes_test(is_admin)
@login_required
def add_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = SessionForm()
    return render(request, 'add_session.html', {'form': form})


@user_passes_test(is_admin)
@login_required
def add_film(request):
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = FilmForm()
    return render(request, 'add_film.html', {'form': form})


@user_passes_test(is_admin)
@login_required
def view_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'view_bookings.html', {'bookings': bookings})


@user_passes_test(is_admin)
@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.session.seats_available += booking.tickets_count
        booking.session.save()
        booking.delete()
        return redirect('view_bookings')
    return render(request, 'delete_booking.html', {'booking': booking})