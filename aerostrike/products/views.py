from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def add_product(request):
    if request.user.role != 'distributor':
        return redirect('dashboard')

    if request.method == 'POST':
        Product.objects.create(
            name=request.POST['name'],
            product_type=request.POST['product_type'],
            description=request.POST['description'],
            price=request.POST['price'],
            range_km=request.POST['range_km'],
            speed=request.POST['speed'],
            image=request.FILES['image'],
            distributor=request.user
        )
        return redirect('dashboard')

    return render(request, 'products/add_product.html')

def product_list(request):
    products = Product.objects.filter(is_approved=True)
    return render(request, 'products/list.html', {'products': products})


