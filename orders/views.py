from django.shortcuts import render

from django.shortcuts import render
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
