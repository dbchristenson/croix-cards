from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # User registration
    path("register/", views.register, name="register"),
    # Card management
    path("add_card/", views.add_card, name="add_card"),
]
