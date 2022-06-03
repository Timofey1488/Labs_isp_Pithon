from django.core.mail import send_mail


def send_message(email, text, topic):
    send_mail(
        topic,
        text,
        'medved20032003@gmail.com',
        [email],
        fail_silently=False
    )
