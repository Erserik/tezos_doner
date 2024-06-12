from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('invite_person/', views.saveprofile, name='invite_person'),
    path('search_users/', views.search_users, name='search_users'),
    path('', views.home, name='home'),
    path('send_invitation/', views.send_invitation, name='send_invitation'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('appointment_success/', views.appointment_success, name='appointment_success'),
    path('load_timeslots/', views.load_timeslots, name='load_timeslots'),
    path('confirm_appointment/', views.confirm_appointment, name='confirm_appointment'),
]
