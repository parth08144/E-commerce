from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user

    if user.role == 'admin':
        return redirect('admin_dashboard')

    elif user.role == 'distributor':
        return redirect('distributor_dashboard')

    elif user.role == 'consumer':
        return redirect('consumer_dashboard')

    return redirect('login')


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('dashboard')

    return render(request, 'dashboard/admin.html')


@login_required
def distributor_dashboard(request):
    if request.user.role != 'distributor':
        return redirect('dashboard')

    return render(request, 'dashboard/distributor.html')


@login_required
def consumer_dashboard(request):
    if request.user.role != 'consumer':
        return redirect('dashboard')

    return render(request, 'dashboard/consumer.html')


