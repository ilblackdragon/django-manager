# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.auth import authenticate
from django.db.models import Count, Q

from auth_ext.models import EmailConfirmation
from auth_ext.forms import LoginForm, SignupForm, ChangePasswordForm, ChangeEmailForm
from auth_ext.utils import get_default_redirect, auth_ext_login
from auth_ext.signals import signup_done

from misc.json_encode import json_template

def login(request, form_class=LoginForm, template_name="auth/login.html", success_url=None):
    if success_url is None:
        success_url = get_default_redirect(request)
    form = form_class(request.POST or None)
    if form.is_valid():
        return auth_ext_login(request, form.user, success_url,
            remember=form.cleaned_data['remember'])
    return direct_to_template(request, template_name, {'form': form})

def logout(request, template_name="auth/logout.html"):
    response = django_logout(request, template_name=template_name)
    response.delete_cookie('logined')
    return response

def signup(request, form_class=SignupForm, template_name="auth/signup.html", success_url=None):
    if success_url is None:
        success_url = get_default_redirect(request)
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username, password = form.save()
        new_user = get_object_or_404(User, username = username)
        signup_done.send(sender=User, user=new_user)
        if settings.ACCOUNT_EMAIL_VERIFICATION:
            return direct_to_template(request, "account/verification_sent.html", {"email": form.cleaned_data["email"]})
        else:
            user = authenticate(username=username, password=password)
            return auth_ext_login(request, user, success_url)
    return direct_to_template(request, template_name, {"form": form})

def send_confirm_email(request):
    EmailConfirmation.objects.send_confirmation(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def confirm_email(request, confirmation_key):
    confirmation_key = confirmation_key.lower()
    email_address = EmailConfirmation.objects.confirm_email(confirmation_key)
    return direct_to_template(request, "emailconfirmation/confirm_email.html", {"email_address": email_address})

def profile_private_edit_email(request, template_email_form_name = 'auth/profile_private_edit_email_form.html'):
    email_form = ChangeEmailForm(request.user, request.POST or None)
    if request.POST.get('action') == 'email':
        if email_form.is_valid():
            email_form.save()
            email_form.data = {'email': ''}
            if request.is_ajax():
                return json_template({'status': 'ok', 'text': _("Email successfully changed.")},
                    template_email_form_name, {'email_form': email_form, 'request': request}) 
            request.user.message_set.create(message=ugettext(u"Email successfully changed."))
        else:
            if request.is_ajax():
                return json_template({'status': 'error', 'text': _('Email changing failed')}, 
                    template_email_form_name, {'email_form': email_form, 'request': request}) 
    if not request.is_ajax():
        return email_form

def profile_private_edit_password(request, template_password_form_name = 'auth/profile_private_edit_password_form.html'):
    password_form = ChangePasswordForm(request.user, request.POST or None)
    if request.POST.get('action') == 'password':
        if password_form.is_valid():
            password_form.save()
            if request.is_ajax():
                return json_template({'status': 'ok', 'text': _("Password successfully changed")},
                    template_password_form_name, {'password_form': password_form}) 
            request.user.message_set.create(message=ugettext(u"Password successfully changed."))
        else:
            if request.is_ajax():
                return json_template({'status': 'error', 'text': _('Password changing failed')}, 
                    template_password_form_name, {'password_form': password_form}) 
    if not request.is_ajax():
        return password_form

def language_change(request, lang):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None) or '/'
    response = redirect(next)
    if lang and lang in map(lambda x: x[0], settings.LANGUAGES):
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            profile.language = lang
            profile.save()
            request.user.message_set.create(message=ugettext(u"Language successfully updated."))
        else:
            max_age = settings.SESSION_MAX_AGE
            if hasattr(request, 'session'):
                request.session.set_expiry(max_age)
                request.session['django_language'] = lang
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang, max_age=max_age)
    return response
