from django.dispatch import Signal

email_confirmed = Signal(providing_args=["user"])
signup_done = Signal(providing_args=["user"])