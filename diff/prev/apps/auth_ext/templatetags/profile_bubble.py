from django.template import Library

register = Library()

@register.inclusion_tag('auth/profile_bubblepopup.html', takes_context=True)
def get_profile_bubblepopup(context, user):
    context['current_user'] = user
    return context
