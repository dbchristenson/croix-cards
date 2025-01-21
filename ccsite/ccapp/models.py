from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=128, null=False, unique=True)
    cards = models.ManyToManyField("Card", through="UserCard")
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)

    # Necessary for avoiding conflicts with AbstractUser default relationships
    groups = models.ManyToManyField(Group, related_name="ccapp_user_set")
    user_permissions = models.ManyToManyField(
        Permission, related_name="ccapp_user_set"
    )

    REQUIRED_FIELDS = ["email", "password"]


class Rarity(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Ability(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return self.name


class Move(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    damage = models.IntegerField()

    energy_requirements = models.ManyToManyField(
        "EnergyType", through="MoveEnergyRequirement"
    )

    def __str__(self):
        return self.name


class CardType(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class CardStage(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class EnergyType(models.Model):
    name = models.CharField(max_length=16)
    symbol = models.ImageField(
        upload_to="energy_symbols/", blank=True, null=True
    )

    def __str__(self):
        return self.name


class MoveEnergyRequirement(models.Model):
    move = models.ForeignKey(Move, on_delete=models.CASCADE)
    energy = models.ForeignKey(EnergyType, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Card(models.Model):
    name = models.CharField(max_length=16)
    description = models.TextField()
    image = models.ImageField(
        upload_to="card_illustrations/", blank=True, null=True
    )

    hitpoints = models.IntegerField()
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)
    stage = models.ForeignKey(CardStage, on_delete=models.CASCADE)
    moves = models.ManyToManyField(Move)
    ability = models.ForeignKey(
        Ability, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.card.name}"


class Collection(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(
        upload_to="collection_illustrations/", blank=True, null=True
    )

    cards = models.ManyToManyField(Card)

    def __str__(self):
        return self.name

    def add_card(self, card):
        self.cards.add(card)
