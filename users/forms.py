from django import forms
from .models import Hospital, TimeSlot, CustomUser

class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'name', 'last_name', 'email', 'iin_number', 'age', 'height', 'weight', 'blood_group', 'description']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class HospitalDateForm(forms.Form):
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), empty_label="Select a hospital")
    date = forms.DateField(widget=forms.SelectDateWidget())

class BookingForm(forms.Form):
    timeslot = forms.ModelChoiceField(queryset=TimeSlot.objects.filter(available=True), empty_label="Select a time slot")
