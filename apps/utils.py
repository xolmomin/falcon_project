import os

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes

from apps.tokens import account_activation_token
from root.settings import EMAIL_HOST_USER


def send_email(subject: str, body: str | None, emails: list[str], html_content=None):
    email = EmailMultiAlternatives(subject=subject, body=body, from_email=EMAIL_HOST_USER, to=emails)
    email.attach_alternative(html_content, "text/html")
    try:
        email.send()
    except Exception as e:
        print(e)

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
def send_registration_link(user, host: str):
    subject = 'Successful Registration'
    token = account_activation_token.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    url = reverse_lazy('confirm_email_page', kwargs={'uidb64': uidb64, 'token': token})
    print(host + url)
    context = {
        'email': user.email,
        'username': user.username,
        'confirm_link': host + url
    }
    html_content = render_to_string('apps/registration_email.html', context)

    send_email(subject, None, [user.email], html_content)

# 10.30.13.224
