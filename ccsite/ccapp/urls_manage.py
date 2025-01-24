from django.urls import path

from . import views

urlpatterns = [
    path("", views.manage, name="manage"),
    path("ability/", views.ability, name="ability"),
    path("ability/new", views.add_ability, name="add_ability"),
    path("move/", views.move, name="move"),
    path("move/new", views.add_move, name="add_move"),
    path("illustrator/", views.illustrator, name="illustrator"),
    path("illustrator/new", views.add_illustrator, name="add_illustrator"),
    path("profile_picture/", views.profile_picture, name="pp"),
    path("profile_picture/new", views.add_profile_picture, name="add_pp"),
    path("collection/", views.collection, name="collection"),
    path("collection/new", views.add_collection, name="add_collection"),
    path("card/", views.card, name="card"),
    path("card/new", views.add_card, name="add_card"),
]
