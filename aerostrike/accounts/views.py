from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User

from django.core.mail import send_mail
from .utils import generate_otp
from django.conf import settings

def signup_view(request): #signup page logic
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        otp = generate_otp()

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.role = role
        user.otp = otp
        user.is_active = False
        user.save()

        send_mail(
            'Your AeroStrike OTP',
            f'Your OTP is {otp}',
            settings.EMAIL_HOST_USER,
            [email],
        )

        request.session['email'] = email
        return redirect('verify_otp')

    return render(request, 'accounts/signup.html')


def login_view(request): #login page logic
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def verify_otp(request): #Verify otp
    if request.method == 'POST':
        otp = request.POST['otp']
        email = request.session.get('email')

        user = User.objects.get(email=email)

        if user.otp == otp:
            user.is_verified = True
            user.is_active = True
            user.otp = ''
            user.save()
            return redirect('login')

    return render(request, 'accounts/verify_otp.html')


