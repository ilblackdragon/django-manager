# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
from random import random

from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.hashcompat import sha_constructor
from django.conf import settings

from auth_ext.signals import email_confirmed
from misc.decorators import receiver

if 'mailer' in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

class EmailConfirmationManager(models.Manager):

    def confirm_email(self, confirmation_key):
        try:
            confirmation = self.get(confirmation_key=confirmation_key)
        except self.model.DoesNotExist:
            return False
        if not confirmation.key_expired():
            profile = confirmation.user.get_profile()
            profile.email_verified = True
            profile.save()
            email_confirmed.send(sender=self.model, user=confirmation.user)
            return True
        return False

    def send_confirmation(self, user):
        salt = sha_constructor(str(random())).hexdigest()[:5]
        confirmation_key = sha_constructor(salt + user.email).hexdigest()
        path = reverse("auth_confirm_email", args=[confirmation_key])
        protocol = getattr(settings, 'MY_SITE_PROTOCOL', 'http')
        port     = getattr(settings, 'MY_SITE_PORT', '')
        activate_url = u"%s://%s%s%s" % (protocol, settings.SITE_DOMAIN, port and ':' + port or '', path)
        context = {
            "user": user,
            "activate_url": activate_url,
            "site_name": settings.SITE_NAME,
            "confirmation_key": confirmation_key,
        }
        subject = render_to_string("auth/email_confirmation_subject.txt", context)
        subject = "".join(subject.splitlines()) # remove superfluous line breaks
        message = render_to_string("auth/email_confirmation_message.txt", context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        profile = user.get_profile()
        profile.email_verified = False
        profile.save()
        return self.create(user=user, sent=datetime.now(), confirmation_key=confirmation_key)

    def delete_expired_confirmations(self):
        for confirmation in self.all():
            if confirmation.key_expired():
                confirmation.delete()

class EmailConfirmation(models.Model):

    user = models.ForeignKey(User)
    sent = models.DateTimeField()
    confirmation_key = models.CharField(max_length=40)

    objects = EmailConfirmationManager()

    def key_expired(self):
        expiration_date = self.sent + timedelta(
            days=settings.EMAIL_CONFIRMATION_DAYS)
        return expiration_date <= datetime.now()

    def __unicode__(self):
        return ugettext("Confirmation for %(user)s, email - %(email)s" % {'user': self.user, 'email': self.user.email})

    class Meta:
        verbose_name = _("E-mail confirmation")
        verbose_name_plural = _("E-mail confirmations")

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=_('User'))
    # Account information
    language = models.CharField(_('language'), max_length=10, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    # Additional information to User
    middle_name = models.CharField(_('Middle name'), max_length=40, default='', blank=True)
    email_verified = models.BooleanField(_('Email confirmed'), default=False)
    
    def __unicode__(self):
        return self.display_name
    
    @models.permalink
    def get_absolute_url(self):
        return ('profile_detail', None, {'username': self.user.username})
    
    @property
    def display_name(self):
        if self.user.first_name and self.user.last_name:
            res = self.user.last_name + ' ' + self.user.first_name
            if self.middle_name:
                res += ' ' + self.middle_name
        else:
            res = self.user.username
        return res
        
    @property
    def get_surname_and_initials_or_nick(self):
        if self.user.last_name and self.user.first_name:
            result = self.user.last_name + ' ' + self.user.first_name[0] + '.'
            if self.middle_name:
                result += ' ' + self.middle_name[0] + '.'
        else:
            result = self.user.username
        return result

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

@receiver(post_save, sender=User)
def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)
