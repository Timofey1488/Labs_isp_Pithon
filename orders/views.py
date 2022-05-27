from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):  # get current session cart
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clearing cart
            cart.clear()
            return render(request, 'orders/created_order.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/create_order.html',
                  {'cart': cart, 'form': form})


class OrderCreationView(FormView):
    form_class = OrderCreateForm
    template_name = "cryptoshop/products/product_detail.html"

    def form_valid(self, form):
        logger.info("use OrderCreationView")

        product_id = self.kwargs['pk']
        order = form.save(commit=False)  # commit=False if we need to create filed ourselves
        order.status = "PENDING"
        order.user = self.request.user
        order.product = get_object_or_404(Product, id=product_id)
        exists_order = Order.objects.filter(user=order.user, product=order.product, status="PENDING")
        if exists_order:
            exists_order[0].amount += order.amount
            exists_order[0].save()
        else:
            order.save()

        return HttpResponseRedirect(reverse_lazy("orders/created_order.html"))

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse_lazy("products"))