from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Product, Category, Cart
from .models import Status
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    if request.user.is_authenticated:
        myorders = Status.objects.filter(user=request.user)
        return render(request, 'store/product_list.html',{'products': products, 'categories':categories, 'myorders':myorders})
    return render(request, 'store/product_list.html',{'products': products, 'categories':categories})

def product_detail(request, pk):
    product = get_list_or_404(Product, pk=pk)[0]
    buy = True
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        products = cart.products.all()
        if product in products:
            buy=False
        return render(request, 'store/product_detail.html',{'product': product, 'buy': buy})
    return render(request, 'store/product_detail.html',{'product': product, 'buy': buy})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password1 = form.cleaned_data.get("password1")
            user = authenticate(username=username,password=password1)
            login(request,user)        
            return redirect('/')
        else:
            a=dict()
            a['form'] = form
            return render(request, 'store/signup.html', context=a)
    else:
        form = SignupForm()   
    a=dict()
    a['form'] = form
    return render(request, 'store/signup.html', context=a)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = LoginForm()
    else:
        form = LoginForm()

    return render(request, "store/login.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='store:login')
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    products = cart.products.all()
    total = 0
    for i in products:
        total += i.price
    return render(request, 'store/cart.html', {'products': products, 'total': total})

@login_required(login_url='store:login')
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    return redirect('store:view_cart')

@login_required(login_url='store:login')
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    cart.products.remove(product)
    return redirect('store:view_cart')

@login_required(login_url='store:login')
def checkout(request):
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)
        products = cart.products.all()
        for i in products:
            x = Status(user=request.user, product=i)
            x.save()
            # x.product.add(i)
            cart.products.remove(i)
            
        return redirect('store:track')
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    products = cart.products.all()
    total = 0
    for i in products:
        total += i.price
    return render(request, 'store/checkout.html', {'total': total})

@login_required(login_url='store:login')
def track(request):
    myorders = Status.objects.filter(user=request.user)
    return render(request, 'store/track.html', {'orders': myorders})

def category(request, category):
    category = get_object_or_404(Category, name=category)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    if request.user.is_authenticated:
        myorders = Status.objects.filter(user=request.user)
        return render(request, 'store/category.html',{'products': products, 'myorders':myorders, 'name': category, 'categories':categories})
    return render(request, 'store/category.html',{'products': products, 'name': category, 'categories':categories})

def about(request):
    return render(request, 'store/aboutme.html')

def contact(request):
    return render(request, 'store/contact.html')







