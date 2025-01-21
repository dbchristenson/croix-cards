from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render

from .forms import AddCardForm, SignInForm, SignUpForm


# Create your views here.
def index(request):
    """View for the index page."""

    # Redirect the user to the home page if they are already logged in
    if request.user.is_authenticated:
        return redirect("home/")

    return render(request, "index.html")


def logout_view(request):
    """View for the logout page that logs the user out."""

    # Check if the user is logged in
    if not request.user.is_authenticated:
        return redirect("/")

    # Log the user out
    logout(request)

    return render(request, "index.html")


### User Registration ###   # noqa: E266
def register(request):
    """Handles registering new accounts."""

    if request.user.is_authenticated:
        return redirect("home")

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

    return render(request, "accounts/register.html", {"form": form})


def sign_in(request):
    """Handles logging in users."""

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignInForm(request.POST, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

        else:
            form.add_error(None, "Invalid username or password.")
    else:
        print("Creating new form.")
        form = SignInForm()

    return render(request, "accounts/sign_in.html", {"form": form})


### General Views ###    # noqa: E266
def home(request):
    """View for the home page."""

    return render(request, "home.html")


### Card Management (Admins) ###    # noqa: E266
def add_card(request):
    """View for the add card page."""

    # Check if the user is an admin
    if not request.user.is_staff:
        return redirect("home")

    if request.method == "POST":
        form = AddCardForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("add_card.html")

    return render(request, "add_card.html")
