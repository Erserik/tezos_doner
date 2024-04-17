from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import SignUpForm, LoginForm

from .tezos_func import Change



def signup(request):
    if request.method == 'POST':

        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Synchronously create blockchain contract
            # Send welcome email
            send_mail(
                'Welcome to Our Site',
                'Thanks for signing up!',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )

            # Redirect to the user's profile page
            return redirect('users:profile')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


# def save_form(request):
#     if request.method == 'POST':
#         form = SaveProfileForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             return redirect('users:profile')
#     else:
#         form = SaveProfileForm()
#     return render(request, 'users/saveprofileform.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        print(Change())
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)  # This authenticates the user and returns a user instance

            if user is not None:
                login(request, user)  # Log in the user
                return redirect('users:profile')
    else:
        form = LoginForm()
    return render(request, 'users/signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('users:signin')

def profile(request):
    return render(request, 'users/profile.html')
