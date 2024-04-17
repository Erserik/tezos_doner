from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('save_form/', views.saveprofile, name='save_form'),
    path('search_users/', views.search_users, name='search_users')
]
