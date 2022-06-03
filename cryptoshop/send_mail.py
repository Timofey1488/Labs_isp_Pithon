from django.core.mail import send_mail


def send_message(email, text, topic):
    send_mail(
        topic,
        text,
        'medved20032003@gmail.com',
        [email],
        fail_silently=False  # errors will be cancel
    )


def send_order_message(user, email, text, order):
    send_mail(
        f"Hi, thank you for order {user}",
        f"{text}"
        f"order: {order}",
        'medved20032003@gmail.com',
        [email],
        fail_silently=False
    )
