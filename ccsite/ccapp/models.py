from datetime import timedelta

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    REQUIRED_FIELDS = ["email", "password"]
    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=128, null=False, unique=True)
    profile_picture = models.ForeignKey(
        "ProfilePicture", on_delete=models.SET_NULL, null=True
    )

    # Card collection and progression tracking
    cards = models.ManyToManyField("Card", through="UserCard")
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)

    # Pack opening tracking
    MAX_PACKS = 5
    PACK_COOLDOWN = timedelta(hours=12)
    available_packs = models.IntegerField(default=0, null=False)
    last_refresh = models.DateTimeField(null=True)
    time_to_next_refresh = models.DurationField(default=timedelta(0))
    pack_hourglasses = models.IntegerField(default=24, null=False)

    # Necessary for avoiding conflicts with AbstractUser default relationships
    groups = models.ManyToManyField(Group, related_name="ccapp_user_set")
    user_permissions = models.ManyToManyField(
        Permission, related_name="ccapp_user_set"
    )

    # Methods
    def refresh_packs(self, cooldown=PACK_COOLDOWN, max_packs=MAX_PACKS):
        """
        Method for tracking and refreshing the user's available packs. When
        called, the method will check for the time since the last time a pack
        was added to the user's account and add packs accordingly.
        """
        time_since_last_refresh = now() - self.last_refresh

        if time_since_last_refresh >= cooldown:
            packs_to_add = time_since_last_refresh // cooldown
            self.last_refresh = now()
            self.available_packs = min(
                self.available_packs + packs_to_add, max_packs
            )

            self.last_refresh = now() - (time_since_last_refresh % cooldown)
        else:
            # Update remaining time to next refresh
            self.time_to_next_refresh = cooldown - time_since_last_refresh

        self.save

    def use_hourglass(self, num_hourglasses: int):
        """
        Uses hourglasses to reduce the cooldown time for a user to receive
        an additional pack. The number of hourglasses used is passed as an
        argument, and the method will calculate whether the user has enough
        hourglasses to use and whether the user can use the hourglasses
        without exceeding the maximum number of packs allowed.
        """
        c1 = self.pack_hourglasses > num_hourglasses
        c2 = self.time_to_next_refresh() > timedelta(minutes=0)

        if c1 and c2:
            # Calculate how many packs would be added
            total_hours = self.MAX_PACKS * self.PACK_COOLDOWN
            time_since_last_refresh = now() - self.last_refresh
            hours_worth_of_packs_held = (
                self.available_packs * self.PACK_COOLDOWN
                + time_since_last_refresh
            )

            available_hours = total_hours - hours_worth_of_packs_held
            packs_that_can_be_added = available_hours // self.PACK_COOLDOWN

            # Print all info
            print(f"Total hours: {total_hours}")
            print(f"Time since last refresh: {time_since_last_refresh}")
            print(f"Hours worth of packs held: {hours_worth_of_packs_held}")
            print(f"Available hours: {available_hours}")
            print(f"Packs that can be added: {packs_that_can_be_added}")

            if self.available_packs + packs_that_can_be_added > self.MAX_PACKS:
                raise ValueError(
                    (
                        f"Using {num_hourglasses} hourglasses would exceed"
                        " maximum number of allowed packs."
                    )
                )

            # Check complete: max available packs is not exceeded
            print("Max available packs not exceeded.")
            self.available_packs += packs_that_can_be_added

        else:
            raise ValueError("Insufficient hourglasses or cannot use one.")


class ProfilePicture(models.Model):
    image = models.ImageField(upload_to="profile_pictures/")

    def __str__(self):
        return self.image.name


class Illustrator(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


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
    illustrator = models.ForeignKey(
        Illustrator, default="", on_delete=models.CASCADE
    )
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
