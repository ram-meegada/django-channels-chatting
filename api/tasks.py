from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from abstractbaseuser_project import settings
from time import sleep
from .models import User

@shared_task
def send_apikey_to_mail(email):
    # sleep(60)
    print(email, '=====================came to function================')
    user = User.objects.all().first()
    context = {"message": "this is testing message", "user":str(user)}
    temp = render_to_string('key.html', context)
    msg = EmailMultiAlternatives(f"Your Api Key", temp, settings.DEFAULT_FROM_EMAIL, [email])
    msg.content_subtype = 'html'
    msg.send()
    print('sent')
    return 'sent'

@shared_task
def add(x, y):
    print('came here==============')
    return x + y