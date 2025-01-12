from django.db import models


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

    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)
    moves = models.ManyToManyField(Move)
    ability = models.ForeignKey(
        Ability, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


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
