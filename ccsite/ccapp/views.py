import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import AddCardForm, SignInForm, SignUpForm
from .models import User


# Create your views here.
def index(request):
    """View for the index page."""

    # Redirect the user to the home page if they are already logged in
    if request.user.is_authenticated:
        return redirect("home/")

    return render(request, "index.html")


def logout_view(request):
    """Handles log outs."""

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


### General Service Views ###   # noqa: E266
@csrf_exempt
def refresh_packs_view(request):
    """
    View to refresh user packs.
    """
    user = request.user  # Assume authentication middleware is in place
    user.refresh_packs()
    return JsonResponse(
        {
            "available_packs": user.available_packs,
            "time_to_next_refresh": user.time_to_next_refresh.total_seconds(),
        }
    )


@csrf_exempt
def use_hourglass_view(request):
    """View to use hourglasses to refresh packs."""
    user = request.user
    data = json.loads(request.body)
    num_hourglasses = data.get("num_hourglasses", 0)

    try:
        user.use_hourglass(num_hourglasses)
        return JsonResponse(
            {"success": True, "available_packs": user.available_packs}
        )
    except ValueError as e:
        return JsonResponse({"success": False, "error": str(e)})


### General Views ###    # noqa: E266
def home(request):
    """View for the home page."""

    return render(request, "home.html")


def profile(request):
    """View for the user profile page."""
    username = request.GET.get("username")
    if username:
        user = get_object_or_404(User, id=username)
    else:
        user = request.user

    return render(request, "accounts/profile.html", {"profile_user": user})


### Card Management (Admins) ###    # noqa: E266
@staff_member_required
def manage(request):
    """View for managing cards."""
    return render(request, "manage/manage.html")


@staff_member_required
def ability(request):
    """View for listing abilities."""
    return render(request, "manage/ability.html")


@staff_member_required
def add_ability(request):
    """View for adding an ability."""
    return render(request, "manage/add_ability.html")


@staff_member_required
def move(request):
    """View for listing moves."""
    return render(request, "manage/move.html")


@staff_member_required
def add_move(request):
    """View for adding a move."""
    return render(request, "manage/add_move.html")


@staff_member_required
def illustrator(request):
    """View for listing illustrators."""
    return render(request, "manage/illustrator.html")


@staff_member_required
def add_illustrator(request):
    """View for adding an illustrator."""
    return render(request, "manage/add_illustrator.html")


@staff_member_required
def profile_picture(request):
    """View for listing profile pictures."""
    return render(request, "manage/profile_picture.html")


@staff_member_required
def add_profile_picture(request):
    """View for adding a profile picture."""
    return render(request, "manage/add_profile_picture.html")


@staff_member_required
def collection(request):
    """View for listing collections."""
    return render(request, "manage/collection.html")


@staff_member_required
def add_collection(request):
    """View for adding a collection."""
    return render(request, "manage/add_collection.html")


@staff_member_required
def card(request):
    """View for listing cards."""
    return render(request, "manage/card.html")


@staff_member_required
def add_card(request):
    """View for adding a card."""
    form = AddCardForm()

    return render(request, "manage/add_card.html", {"form": form})
