from django.core.mail import send_mail


def send_message(email, text, topic):
    send_mail(
        topic,
        text,
        'medved20032003@gmail.com',
        [email],
        fail_silently=False  # errors will be cancel
    )


def send_order_message(user, email, text, order, total):
    send_mail(
        f"Hi, thank you for order {user}",
        f"Your products:\n"
        f"{text}\n"
        f"Order number: {order}\n"
        f"Total price: {total}\n"
        f"We will contact you soon",
        'medved20032003@gmail.com',
        [email],
        fail_silently=False
    )
