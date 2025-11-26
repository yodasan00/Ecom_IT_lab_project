from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


def login(request):
    if request.method == "POST":
        email = request.POST.get('emailid')
        password = request.POST.get('passid')

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                messages.success(request, "Login successful!")
                return redirect('index') 
            else:
                messages.error(request, "Invalid password.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")

    return render(request, "login.html") 


def register(request):
    if request.method == "POST":
        username = request.POST.get('Username')
        email = request.POST.get('emailid')
        password = request.POST.get('passid')

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            messages.error(request, "User with this email or username already exists.")
        else:
            user = User(username=username, email=email, password=make_password(password))
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")  

    return render(request, "register.html")  

def index(request):
    return render(request, "index.html")