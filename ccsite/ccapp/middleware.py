from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip authentication check for the index, sign_in, and register pages
        excluded_paths = [
            reverse("index"),
            reverse("sign_in"),
            reverse("register"),
        ]
        if (
            not request.user.is_authenticated
            and request.path not in excluded_paths
        ):
            return redirect("index")
        return self.get_response(request)
