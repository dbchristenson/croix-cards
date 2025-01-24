from django.urls import path

from . import views

urlpatterns = [
    path("", views.manage_cards, name="manage_cards"),
    path("add_card/", views.add_card, name="add_card"),
]
