from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Hospital, HospitalManager, TimeSlot, Appointment
from .forms import SignUpForm, LoginForm, ContactForm, HospitalDateForm, BookingForm
from django.db.models import Q
from django.contrib.auth import logout, authenticate, login

from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, get_user_model
from .models import Hospital, HospitalManager, TimeSlot, Appointment, CustomUser, Invitation
from .forms import SignUpForm, LoginForm, ContactForm, HospitalDateForm, BookingForm
from django.db.models import Q
from datetime import datetime, timedelta

from .tezos_func import Create_manual, Change, Create

def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                f'Message from {name} gmail:"{email}"',
                message,
                email,
                ['erserikdaryn82@gmail.com'],  # Your email address
                fail_silently=False,
            )

            return render(request, 'users/home.html', {'form': form, 'success': True})
    else:
        form = ContactForm()

    return render(request, 'users/home.html', {'form': form})


def search_users(request):
    query = request.GET.get('query', '')
    blood_group_filter = request.GET.get('blood_group', '')

    users = get_user_model().objects.all()

    if query:
        users = users.filter(
            Q(blockchain_contract_id__icontains=query) |
            Q(name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(iin_number__icontains=query) |
            Q(age__icontains=query) |
            Q(height__icontains=query) |
            Q(weight__icontains=query) |
            Q(description__icontains=query)
        )

    if blood_group_filter:
        users = users.filter(blood_group__icontains=blood_group_filter)

    results = [{'name': user.name, 'last_name': user.last_name, 'email': user.email, 'blood_group': user.blood_group} for user in users]

    return JsonResponse({'results': results})



def signup(request):
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(Create())
            print(form.cleaned_data['age'])
            print(form.cleaned_data['height'])
            print(form.cleaned_data['weight'])
            print(form.cleaned_data['blood_group'])
            print(form.cleaned_data['description'])
            contract = Create_manual()
            print('#' + contract + '#')
            text = 'age:' + str(form.cleaned_data['age']) + ' height:' + str(
                form.cleaned_data['height']) + ' weight:' + str(form.cleaned_data['weight']) + ' blood group:' + str(
                form.cleaned_data['blood_group']) + ' description:' + str(form.cleaned_data['description'])
            Change(contract, text)

            user = form.save()
            user.blockchain_contract_id = contract
            user.save()

            send_mail(
                'Welcome to Our Site',
                'Thanks for signing up!',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )

            login(request, user)
            return redirect('users:profile')
    else:
        form = SignUpForm()

    return render(request, 'users/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:profile')
    else:
        form = LoginForm()
    return render(request, 'users/signin.html', {'form': form})


def signout(request):
    logout(request)
    return render(request, 'users/home.html')


@login_required
def profile(request):
    return render(request, 'users/profile.html')


def saveprofile(request):
    return render(request, 'users/saveprofileform.html')


@login_required
def send_invitation(request):
    email = request.GET.get('email', '')
    date = request.GET.get('date', '')
    time = request.GET.get('time', '')
    blood_group = request.GET.get('blood_group', '')

    user = request.user
    hospital_manager = HospitalManager.objects.get(user=user)
    hospital = hospital_manager.hospital

    invited_user = CustomUser.objects.filter(email=email).first()

    if invited_user:
        invitation = Invitation.objects.create(
            email=email,
            date=date,
            time=time,
            hospital=hospital,
            blood_group=blood_group,
            invited_user=invited_user,
            sent_by=user
        )

        send_mail(
            'Invitation to Hospital Visit',
            f"Dear {invited_user.name},\n\nWe are pleased to invite you to Hospital {hospital.name}, located at {hospital.address}, on {date} at {time} for a blood donation session. Your participation is crucial to help those in need.\n\nBest regards,\n{hospital.name} Team",
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return JsonResponse({'message': f'Invitation sent successfully to {email} for {date} at {time}'})
    else:
        return JsonResponse({'message': 'User not found.'}, status=404)


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = HospitalDateForm(request.POST)
        if form.is_valid():
            hospital = form.cleaned_data['hospital']
            date = form.cleaned_data['date']
            generate_time_slots(hospital, date, date)  # Generate time slots for the selected date
            timeslots = TimeSlot.objects.filter(hospital=hospital, date=date, available=True)
            booking_form = BookingForm()
            booking_form.fields['timeslot'].queryset = timeslots
            return render(request, 'users/book_appointment.html',
                          {'form': form, 'booking_form': booking_form, 'timeslots': timeslots})
    else:
        form = HospitalDateForm()

    return render(request, 'users/book_appointment.html', {'form': form})


@login_required
def confirm_appointment(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            timeslot = form.cleaned_data['timeslot']
            timeslot.available = False
            timeslot.save()
            appointment = Appointment.objects.create(user=request.user, timeslot=timeslot, hospital=timeslot.hospital)

            # Send confirmation email
            send_mail(
                'Appointment Confirmation',
                f"Dear {request.user.name},\n\nYour appointment at {appointment.hospital.name} located at {appointment.hospital.address} has been confirmed for {timeslot.date} from {timeslot.start_time} to {timeslot.end_time}.\n\nThank you for booking with us!\n\nBest regards,\n{appointment.hospital.name} Team",
                'from@example.com',
                [request.user.email],
                fail_silently=False,
            )

            return redirect('users:appointment_success')
    return redirect('users:book_appointment')


@login_required
def appointment_success(request):
    return render(request, 'users/appointment_success.html')


def load_timeslots(request):
    hospital_id = request.GET.get('hospital')
    date = request.GET.get('date')
    timeslots = TimeSlot.objects.filter(hospital_id=hospital_id, date=date, available=True).values('id', 'start_time',
                                                                                                   'end_time')
    return JsonResponse(list(timeslots), safe=False)


def generate_time_slots(hospital, start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        for hour in range(10, 21):
            start_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=hour)
            end_time = start_time + timedelta(hours=1)
            TimeSlot.objects.get_or_create(
                hospital=hospital,
                date=current_date,
                start_time=start_time.time(),
                end_time=end_time.time(),
                available=True
            )
        current_date += timedelta(days=1)
