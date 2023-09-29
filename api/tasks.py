from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from abstractbaseuser_project import settings

@shared_task
def send_apikey_to_mail(email, generated_api_key):
    print(email, '=====================came to function================')
    context = {"apikey":generated_api_key}
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