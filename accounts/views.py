from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm

# Create your views here.

def index(request):
    return render(request, "index.html")

def myadmin(request):
    return render(request, "admin.html")

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "success_ LoggedOut.")
    return redirect(reverse('index'))  

def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
        if user:
            auth.login(user=user, request=request)
            messages.success(request, "User... loggedIN")         
            return redirect(reverse('index'))                           
        else:
            login_form.add_error(None, "Username or Password Inncorrect")    
    else:
        login_form = UserLoginForm()        
    return render(request, 'login.html', {"login_form": login_form})

def registration(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()    
            user = auth.authenticate(username=request.POST['username'],
                                     password1=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "newUser Thank you for registering")
                return redirect(reverse('index'))
            else:
                messages.error(request, "Registration failed please try again later.")    
    registration_form = UserRegistrationForm()
    return render(request, 'registration.html',{
        "registration_form": registration_form
    })    

def user_profile(request):
    user = User.objects.get(email=request.user.email)    
    return render(request, 'profile.html', {"profile":user})