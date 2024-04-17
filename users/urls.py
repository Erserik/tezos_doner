from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    # path('save_form', views.save_form, name='save_form')
]
