from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy

from cart.forms import CartAddProductForm
from django.contrib import messages

import logging

from django.shortcuts import render, get_object_or_404

from orders.forms import OrderCreateForm
from orders.models import Order
from .forms import UserRegisterForm
from .models import Category, Product
from django.views.generic import ListView, DetailView, FormView

logger = logging.getLogger("main_logger")


class CategoryListView(ListView):
    template_name = "cryptoshop/product/list.html"
    model = Category
    context_object_name = 'categories'
    logger.info("use CategoryListView")


class CategoryDetailView(ListView):
    template_name = "cryptoshop/category_detail.html"
    model = Product
    context_object_name = 'products'
    logger.info("use CategoryDetailView")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']

        return context

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['pk']).select_related('category')


class ProductDetailView(DetailView):
    template_name = "cryptoshop/product/detail.html"
    model = Product
    context_object_name = 'product'
    logger.info("use ProductDetailView")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddProductForm

        return context


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'cryptoshop/product/detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    logger.info("use product_list")
    return render(request,
                  'cryptoshop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


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
