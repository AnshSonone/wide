from django.utils.encoding import smart_str, force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings

def encode_url(user, route):
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    link = reverse(route, kwargs={'uid': uid, 'token': token})
    url = f'{settings.SITE_DOMAIN}{link}'
    return url

def decode_url(uid):
    user_id = force_str(urlsafe_base64_decode(uid))
    return user_id

def get_token(user, token):
    value = default_token_generator.check_token(user, token)
    return value