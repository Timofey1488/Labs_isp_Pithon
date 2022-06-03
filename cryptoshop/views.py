from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from cart.forms import CartAddProductForm

import logging

from django.shortcuts import render, get_object_or_404
from .send_mail import send_message
from .tasks import send_message_async

from .forms import UserRegisterForm, ProductNewForm, ProfileForm, WriteNewsForm
from .models import Category, Product, Profile
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

logger = logging.getLogger("main_logger")
logger.setLevel(logging.DEBUG)


class ProductListView(ListView):
    template_name = "cryptoshop/product/list.html"
    model = Product
    context_object_name = 'products'
    logger.info("use ProductListView")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class UpdateProduct(UpdateView):
    model = Product
    form_class = ProductNewForm
    template_name = 'cryptoshop/crud/edit.html'
    success_url = reverse_lazy('cryptoshop:product_list')
    logger.info("use UpdateProduct")


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
        context['category'] = Product.objects.get(pk=self.kwargs['pk']).category
        print(Product.objects.get(pk=self.kwargs['pk']).category)

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


class RegisterUserView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "cryptoshop/register.html"
    logger.info("use RegisterUserView")
    success_message = 'Account successfully created'

    def form_valid(self, form):
        user = form.save()
        image = form.cleaned_data.get('image')
        address = form.cleaned_data.get('address')
        email = form.cleaned_data.get('email')
        profile = Profile()
        profile.user = user
        profile.profile_pic = image
        profile.address = address
        profile.email = email
        user.save()
        profile.save()

        return HttpResponseRedirect(reverse_lazy('cryptoshop:product_list'))


class ShowProfileView(DetailView):
    model = Profile
    template_name = "cryptoshop/personal_profile.html"
    context_object_name = 'profile'
    logger.info("use ShowProfileView")

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).select_related('user')


class CreateNewProduct(CreateView):
    logger.info("use CreateNewProduct")
    form_class = ProductNewForm
    template_name = 'cryptoshop/crud/add_new.html'
    success_url = reverse_lazy('cryptoshop:product_list')


class DeleteProduct(DeleteView):
    logger.info("use DeleteOrderView")
    model = Product
    template_name = 'cryptoshop/crud/delete.html'
    success_url = reverse_lazy("cryptoshop:product_list")


def product_detail(request, pk):
    logger.info("use ProductDetailView")
    product = get_object_or_404(Product,
                                pk=pk,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'cryptoshop/product/detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})


def product_list(request, category_slug=None):
    logger.info("use ProductListView")
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


class PasswordChangingView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "profile/change_password.html"
    logger.info("use PasswordChangingView")

    def get_success_url(self):
        return reverse_lazy("cryptoshop:profile", kwargs={'pk': self.kwargs['pk']})


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "profile/edit_profile.html"
    form_class = ProfileForm
    logger.info("use EditProfileView")

    def get_success_url(self):
        return reverse_lazy("cryptoshop:profile", kwargs={'pk': self.kwargs['pk']})


def write_news(request):
    if request.method == 'POST':
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            topic = form.cleaned_data['topic']
            users = User.objects.all()
            for user in users:
                if user.email is not '':
                    # send_message('testispasync1234@gmail.com', text, topic)
                    send_message_async.delay(user.email, text, topic)
            return HttpResponseRedirect(reverse_lazy('cryptoshop:product_list'))

    else:
        form = WriteNewsForm()

    return render(request, 'cryptoshop/write_news.html', {'form': form})
