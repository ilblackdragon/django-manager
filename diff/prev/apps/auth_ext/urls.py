from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('auth_ext.views',
    # Sign up, Login and Logout
    url(r'^signup/$', 'signup', name="auth_signup"),
    url(r'^login/$', 'login', name="auth_login"),
    url(r'^logout/$', 'logout', name="auth_logout"),
    # Email confirmation
    url(r'^confirmation/send/$', 'send_confirm_email', name='auth_email_confirmation'),
    url(r'^confirm_email/(\w+)/$', 'confirm_email', name="auth_confirm_email"),
    url(r'^language/(?P<lang>\w+)/$', 'language_change', name="auth_language_change"),
)

# Password reset (django.contib.auth urls redefinition)
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^password_reset/$', 'password_reset', 
        {'template_name': 'auth/password_reset_form.html', 'email_template_name': 'auth/password_reset_email.html'}, name="auth_password_reset"),
    url(r'^password_reset_done/$', 'password_reset_done', 
        {'template_name': 'auth/password_reset_done.html'}, name="auth_password_reset_done"),
    url(r'^password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm', 
        {'template_name': 'auth/password_reset_confirm.html'}, name="auth_password_reset_confirm"),
    url(r'^password_reset_complete/$', 'password_reset_complete', 
        {'template_name': 'auth/password_reset_complete.html'}, name="auth_password_reset_complete"),
)
