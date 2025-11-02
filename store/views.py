from django.shortcuts import render,get_object_or_404,redirect
from .models import Category
from.models import Product
from django.contrib.auth import login
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Category




def product_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)  # Replace Category with your actual model
    return render(request, 'details.html', {'category':category})
def add_to_cart(request, item_id):
    item = get_object_or_404(Category, pk=item_id)
    cart = request.session.get('cart',{})
    key = str(item_id)
    
    if key in cart:
        cart[key]['quantity'] +=1
    else:
        cart[key] = {
            'name':item.name,
            'image':item.image.url,
            'price':float(item.price),
            'quantity':1,
        }
    request.session['cart'] = cart
    return redirect('home')
def get_cart_total(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return total
def cart_view(request):
    cart=request.session.get('cart',{})
    total=sum(item['price']*item['quantity']for item in cart.values())
    return render(request, 'cart.html',{
        "cart":cart, "total":total
    })

def product_list(request):
    phones = Category.objects.filter(product__name="phones")
    clothes = Category.objects.filter(product__name="clothes")
    watches = Category.objects.filter(product__name="watches")
    screens = Category.objects.filter(product__name="screens")
    
    
    return render(request,'index.html',{
        "phones":phones, "clothes":clothes,"watches":watches,"screens":screens
    })

def login_view(request):
    if request.method =='POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "invalid username or password")
            return render(request,"login.html")
        
    return render(request, "login.html")

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")  # Replace with your homepage
        else:
            messages.error(request,"Enter  valid username")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html',{'form':form})

def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    pk = str(pk)  # convert to string since session keys are strings

    if pk in cart:
        if cart[pk]['quantity'] > 1:
            cart[pk]['quantity'] -= 1
        else:
            del cart[pk]

    request.session['cart'] = cart
    return redirect('cart')
from django.shortcuts import render

def process_mpesa(request):
    if request.method == 'POST':
        mpesa_number = request.POST.get('mpesa_number')
        # You can process the number or store it here
        return render(request, 'payment.html', {'mpesa_number': mpesa_number})
    else:
        return render(request, 'payment.html')
def mpesa_payment(request):
    return render(request, 'payment.html')

def payment_view(request):
    total = request.session.get('cart_total', 0)

    return render(request, 'payment.html', {
        'amount': total,
    })
def about(request):
        return render(request, 'about.html')

    
def home(request):
    query = request.GET.get('q')
    if query:
        phones = Product.objects.filter(category__name='phones', name__icontains=query)
        clothes = Product.objects.filter(category__name='clothes', name__icontains=query)
        watches = Product.objects.filter(category__name='watches', name__icontains=query)
        screens = Product.objects.filter(category__name='screens', name__icontains=query)
    else:
        phones = Product.objects.filter(category__name='phones')
        clothes = Product.objects.filter(category__name='clothes')
        watches = Product.objects.filter(category__name='watches')
        screens = Product.objects.filter(category__name='screens')

    context = {
        'phones': phones,
        'clothes': clothes,
        'watches': watches,
        'screens': screens,
    }
    return render(request, 'index.html', context)




