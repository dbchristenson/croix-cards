from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # User registration
    path("register/", views.register, name="register"),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("logout/", views.logout_view, name="logout"),
    # User stuff
    path("profile/", views.profile, name="profile"),
    # Home page
    path("home/", views.home, name="home"),
]
