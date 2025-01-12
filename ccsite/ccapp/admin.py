from django.contrib import admin

# Register your models here.
from .models import (
    Ability,
    Card,
    CardType,
    EnergyType,
    Move,
    MoveEnergyRequirement,
    Rarity,
)

admin.site.register(Ability)
admin.site.register(Card)
admin.site.register(CardType)
admin.site.register(EnergyType)
admin.site.register(Move)
admin.site.register(MoveEnergyRequirement)
admin.site.register(Rarity)
