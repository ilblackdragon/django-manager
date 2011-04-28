from django.contrib import admin
from auth_ext.models import EmailConfirmation, Profile

admin.site.register(EmailConfirmation)
admin.site.register(Profile)
