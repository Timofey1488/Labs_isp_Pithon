from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from cart.forms import CartAddProductForm

import logging

from django.shortcuts import render, get_object_or_404


from .forms import UserRegisterForm
from .models import Category, Product, Profile
from django.views.generic import ListView, DetailView, FormView, CreateView

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


class RegisterUserView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "cryptoshop/register.html"
    logger.info("use RegisterUserView")
    success_message = 'Account successfully created'

    def form_valid(self, form):
        user = form.save()
        profile = Profile()
        profile.user = user
        user.save()
        profile.save()
        #login(self.request.user)

        return HttpResponseRedirect(reverse_lazy('cryptoshop:product_list'))


class ShowProfileView(DetailView):
    model = Profile
    template_name = "cryptoshop/personal_profile.html"
    context_object_name = 'profile'
    logger.info("use ShowProfileView")

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).select_related('user')
