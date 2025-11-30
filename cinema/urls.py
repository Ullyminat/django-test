from django.urls import path
from . import views

urlpatterns = [
    path('', views.sessions_list, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('sessions/', views.sessions_list, name='sessions_list'),
    path('book/<int:session_id>/', views.book_session, name='book_session'),
    path('profile/', views.profile, name='profile'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/add-session/', views.add_session, name='add_session'),
    path('admin-panel/add-film/', views.add_film, name='add_film'),
    path('admin-panel/bookings/', views.view_bookings, name='view_bookings'),
    path('admin-panel/delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]