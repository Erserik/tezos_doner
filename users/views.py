from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.db.models import Q
from .forms import SignUpForm, LoginForm

from .tezos_func import Create_manual, Change


def search_users(request):
    query = request.GET.get('query', '')
    if query:
        users = get_user_model().objects.filter(
            Q(blockchain_contract_id__icontains=query) |
            Q(name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(iin_number__icontains=query) |
            Q(age__icontains=query) |
            Q(height__icontains=query) |
            Q(weight__icontains=query) |
            Q(blood_group__icontains=query) |
            Q(description__icontains=query)
        )
        results = [{'name': user.name, 'last_name': user.last_name, 'email': user.email} for user in users]
        return JsonResponse({'results': results})
    else:
        return JsonResponse({'results': []})


def signup(request):
    # Проверяем, залогинен ли уже пользователь
    if request.user.is_authenticated:
        # Если пользователь залогинен, перенаправляем его на страницу профиля
        return redirect('users:profile')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['age'])
            print(form.cleaned_data['height'])
            print(form.cleaned_data['weight'])
            print(form.cleaned_data['blood_group'])
            print(form.cleaned_data['description'])
            contract = Create_manual()
            print('#' + contract + '#')
            text = 'age:' + str(form.cleaned_data['age']) + ' height:' + str(form.cleaned_data['height']) + ' weight:' + str(form.cleaned_data['weight']) + ' blood group:' + str(form.cleaned_data['blood_group']) + ' description:' + str(form.cleaned_data['description'])
            Change(contract, text)

            user = form.save()
            user.blockchain_contract_id = contract
            user.save()

            # Synchronously create blockchain contract.txt
            # Send welcome email
            send_mail(
                'Welcome to Our Site',
                'Thanks for signing up!',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )


            # Redirect to the user's profile page
            login(request, user)
            return redirect('users:profile')
    else:
        # Если пользователь не залогинен, но есть аккаунт, перенаправляем на страницу входа
        if get_user_model().objects.filter(username=request.POST.get('username')).exists():
            return redirect('users:signin')
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


def saveprofile(request):
    return render(request, 'users/saveprofileform.html')


