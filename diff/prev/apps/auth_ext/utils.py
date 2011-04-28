# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

LOGIN_REDIRECT_URLNAME = getattr(settings, "LOGIN_REDIRECT_URLNAME", '')

def get_default_redirect(request, redirect_field_name="next",
        login_redirect_urlname=LOGIN_REDIRECT_URLNAME):
    """
    Returns the URL to be used in login procedures by looking at different
    values in the following order:
    
    - LOGIN_REDIRECT_URLNAME - the name of a URLconf entry in the settings
    - LOGIN_REDIRECT_URL - the URL in the setting
    - a REQUEST value, GET or POST, named "next" by default.
    """
    if login_redirect_urlname:
        default_redirect_to = reverse(login_redirect_urlname)
    else:
        default_redirect_to = settings.LOGIN_REDIRECT_URL
    redirect_to = request.REQUEST.get(redirect_field_name)
    # light security check -- make sure redirect_to isn't garabage.
    if not redirect_to or "://" in redirect_to or " " in redirect_to:
        redirect_to = default_redirect_to
    return redirect_to

def auth_ext_login(request, user, success_url, remember=False):
    auth_login(request, user)
    response = redirect(success_url)
    if remember:
        max_age = settings.SESSION_MAX_AGE
        request.session.set_expiry(max_age)
        response.set_cookie('logined', 'true', max_age=max_age)
    else:
        request.session.set_expiry(0)
        response.set_cookie('logined', 'true')
    return response
