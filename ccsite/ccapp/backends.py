from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import User


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"Attempting to authenticate: {username}")
        try:
            user = User.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).first()  # Prevents MultipleObjectsReturned
            if user and user.check_password(password):
                print(f"Authentication successful for user: {user.username}")
                return user
        except User.DoesNotExist:
            print("No such user found.")
        except ValidationError as e:
            print(f"Validation error: {e}")
        return None
