from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render

from .forms import AddCardForm, SignUpForm


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

    return render(request, "index.html")


### User Registration ###   # noqa: E266
def register(request):
    """Handles registering new accounts."""

    if request.method == "POST":
        form = SignUpForm(request.POST)

        try:
            if form.is_valid():
                form.save()

                # Log the user in
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(
                    request, username=username, password=password
                )

                login(request, user)
                return redirect("index")

        except IntegrityError as e:
            if "username" in str(e):
                form.add_error("username", "Username already taken.")
            elif "email" in str(e):
                form.add_error("email", "Email already taken.")
            else:
                form.add_error(None, str(e))
    else:
        form = SignUpForm()

    return render(request, "register.html", {"form": form})


### Card Management (Admins) ###    # noqa: E266
@login_required
def add_card(request):
    """View for the add card page."""

    if request.method == "POST":
        form = AddCardForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("add_card.html")

    return render(request, "add_card.html")
