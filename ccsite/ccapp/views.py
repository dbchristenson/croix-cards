from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


# Create your views here.
def index(request):
    return render(request, "index.html")


def logout_view(request):
    """View for the logout page that logs the user out."""

    # Check the user is logged in
    if not request.user.is_authenticated:
        return redirect("/")

    # Log the user out
    logout(request)

    return render(request, "app/index.html")


### User Registration ###
