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

        # Normalize the current path
        current_path = request.path_info

        if (
            not request.user.is_authenticated
            and current_path not in excluded_paths
        ):
            print(f"Redirecting unauth user from {request.path} to index")
            print(f"MW Session Key After Login: {request.session.session_key}")
            return redirect("index")

        return self.get_response(request)
