from django.contrib.auth import login
from django.shortcuts import redirect
from cart.forms import CartAddProductForm
from django.contrib import messages

# Create your views here.

from django.shortcuts import render, get_object_or_404

from .forms import UserRegisterForm
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'cryptoshop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'cryptoshop/product/detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}')
            return redirect('cryptoshop:product_list')
    else:
        form = UserRegisterForm()
    return render(request, 'cryptoshop/register.html', {'form': form})
