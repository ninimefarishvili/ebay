from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError


def home(request):
    products = Product.objects.all()  
    print(products)  
    return render(request, 'home.html', {'products': products})


def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

@login_required
def create_product(request):
    if request.method == 'POST':
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category_id = request.POST.get('category')
        img_url = request.POST.get('img_url')

        
        if not all([title, description, price, quantity, category_id, img_url]):
            messages.error(request, "All fields must be filled.")
            return redirect('create_product')  

        try:
            
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Selected category does not exist.")
            return redirect('create_product')

        
        product = Product(
            title=title,
            description=description,
            price=price,
            quantity=quantity,
            category=category,
            seller=request.user,  
            img_url=img_url
        )
        product.save()

        messages.success(request, "Product created successfully.")
        return redirect('home')  
    
    categories = Category.objects.all()  
    return render(request, 'create_product.html', {'categories': categories})

@login_required
def add_to_cart(request, product_id):
    
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user)

    try:
        cart.add_to_cart(product)
        messages.success(request, "Product added to cart.")
    except ValidationError as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('home')

@login_required
def view_cart(request):
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    return render(request, "cart.html", {"cart": cart})


def create_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category_id = request.POST.get('category')
        img_url = request.POST.get('img_url')

        category = Category.objects.get(id=category_id)

        
        new_product = Product(
            title=title,
            description=description,
            price=price,
            quantity=quantity,
            category=category,
            img_url=img_url
        )
        new_product.save()

        
        return redirect('home') 

    
    categories = Category.objects.all() 
    return render(request, 'create_product.html', {'categories': categories})