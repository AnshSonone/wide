from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.decorators import sync_and_async_middleware

# @sync_and_async_middleware
def send_activation_email(recipients_email, activation_url):
    subject = 'Activate your account on '+ settings.SITE_DOMAIN
    from_email = settings.EMAIL_HOST_USER
    to = [recipients_email]

    html_content = render_to_string('account/activation_email.html', {'activation_url': activation_url})

    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text/html')
    email.send()
    
    
def send_forgot_password_email(recipients_email, forgot_url):
    subject = 'Reset your password '+ settings.SITE_DOMAIN
    from_email = settings.EMAIL_HOST_USER
    to = [recipients_email]
    
    html_content = render_to_string('account/forgot_password.html', {'forgot_url', forgot_url})

    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text.html')
    email.send()    

def send_notify_email(recipients_email):
    subject = 'Login activity detected on your account '
    from_email = settings.EMAIL_HOST_USER
    to = [recipients_email]
    
    html_content = render_to_string('account/login_activity.html')

    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text.html')
    email.send()
    

