from django.shortcuts import render

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from cryptoshop.send_mail import send_order_message


def order_create(request):  # get current session cart
    cart = Cart(request)
    text = []
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                item_product = item['product']
                item_price = item['price']
                item_count = item['quantity']
                text.append(f'{item_product}:{item_price}x{item_count}')
            my_str = ', '.join(text)
            total = cart.get_total_price()
            send_order_message(order.first_name, order.email, my_str, order.id, total)
            # clearing cart
            cart.clear()
            return render(request, 'orders/created_order.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/create_order.html',
                  {'cart': cart, 'form': form})


