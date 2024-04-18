from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email','name', 'last_name', 'iin_number','age','height','weight','blood_group','description', 'password1', 'password2')

# class SaveProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'iin_number','age','height','weight','blood_group','description')

class LoginForm(AuthenticationForm):
    pass
