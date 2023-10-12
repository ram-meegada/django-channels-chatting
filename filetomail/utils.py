from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
import smtplib
from pdf_mail import sendpdf
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os

# code for html template email automation
def send_image_to_mail(img_url, first_name):
    create_template(img_url, first_name)
    sender = "stefenwarner13@gmail.com"
    receiver = "ramumeegada18@gmail.com"
    message = MIMEMultipart("alternatives")
    message['From'] = sender
    message['Subject'] = "html template"
    message['To'] = receiver
    message['content'] = 'html'
    html_page = r"demo.html"
    with open(html_page, 'r') as html:
        temp = html.read()
    message.attach(MIMEText(temp, 'html'))
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as mail:
        mail.login(sender, 'iyutbwcpmhehhmuc')
        mail.send_message(message)
    print('sent')

# creating the temporary html template and saving it in same directory as "demo.html"
def create_template(img_url, first_name):
    file_html = open("demo.html", "w")
    file_html.write('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>img to mail</title>
    </head>
    <body>
        <h1> hello user </h1>
        <h2>hello {}</h2><br>
        <a href={}>your image</a><br><br>
        <img src={} alt={} height="200" width="300">
    </body>
    </html>'''.format(first_name, f"http://127.0.0.1:8000{img_url}", f"https://i.postimg.cc/Pq9pwNPY/kane.jpg", first_name))
    file_html.close()


def send_pdf_to_mail(pdf_loc, pdf_name):
    obj = sendpdf(
        "stefenwarner13@gmail.com",
        "ram9014@yopmail.com",
        "iyutbwcpmhehhmuc",
        "pdf document",
        "this is a body",
        f"{pdf_name}",
        f"{pdf_loc}"
    )

    obj.email_send()
    print("done")