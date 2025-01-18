from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip authentication check for the index page or login page
        excluded_paths = [
            reverse("index"),
            reverse("login"),
            reverse("register"),
        ]  # Add paths that don't require login
        if (
            not request.user.is_authenticated
            and request.path not in excluded_paths
        ):
            return redirect("index")
        return self.get_response(request)
