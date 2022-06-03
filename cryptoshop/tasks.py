from lab3_cryptoshop.celery import app
from .send_mail import send_message


@app.task
def send_message_async(email, text, topic):
    send_message(email, text, topic)
