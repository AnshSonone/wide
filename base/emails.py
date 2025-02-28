from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_activation_email(recipents_email, activation_url):
    subject = 'Activate your account on '+ settings.SITE_DOMAIN
    from_email = settings.EMAIL_HOST_ADDRESS
    to = [recipents_email]
    
    html_content = render_to_string('account/activation_email.html', {'activation_url': activation_url})

    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text/html')
    email.send()
    
    
def send_forgot_password_email(recipents_email, forgot_url):
    subject = 'Reset your password '+ settings.SITE_DOMAIN
    from_email = settings.EMAIL_HOST_ADDRESS
    to = [recipents_email]
    
    html_content = render_to_string('account/forgot_password.html', {'forgot_url', forgot_url})

    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text.html')
    email.send()    

def send_notify_email(recipents_email):
    subject = 'Login activity detected on your account '
    from_email = settings.EMAIL_HOST_ADDRESS
    to = [recipents_email]
    
    html_content = render_to_string('account/login_activity.html', {'recipents_email', recipents_email})

    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text.html')
    email.send()
    

