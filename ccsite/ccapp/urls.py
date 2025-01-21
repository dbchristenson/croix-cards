from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # User registration
    path("register/", views.register, name="register"),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("logout/", views.logout_view, name="logout"),
    # Home page
    path("home/", views.home, name="home"),
    # Card management
    path("add_card/", views.add_card, name="add_card"),
]
