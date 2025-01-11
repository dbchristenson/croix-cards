from django.db import models


class Rarity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Move(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    damage = models.IntegerField()


class CardType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")

    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)
    moves = models.ManyToManyField(Move)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")

    cards = models.ManyToManyField(Card)

    def __str__(self):
        return self.name
