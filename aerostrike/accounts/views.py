from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User

from django.core.mail import send_mail
from .utils import generate_otp
from django.conf import settings
from django.contrib import messages

def signup_view(request):  # signup page logic
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        # ✅ CHECK username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

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


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            if not user.is_verified:
                messages.error(request, "Please verify OTP first")
                return redirect('login')

            login(request, user)
            return redirect('dashboard')

        messages.error(request, "Invalid credentials")
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def verify_otp(request):  # Verify OTP
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('email')

        if not email:
            return redirect('signup')

        # SAFE: handles duplicate emails
        user = User.objects.filter(email=email).order_by('-id').first()

        if not user:
            messages.error(request, "User not found")
            return redirect('signup')

        if user.otp == otp:
            user.is_verified = True
            user.is_active = True
            user.otp = ''
            user.save()
            return redirect('login')

        messages.error(request, "Invalid OTP")

    return render(request, 'accounts/verify_otp.html')



