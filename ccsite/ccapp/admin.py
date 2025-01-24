from django.contrib import admin

# Register your models here.
from .models import (
    Ability,
    Card,
    CardStage,
    CardType,
    Collection,
    EnergyType,
    Illustrator,
    Move,
    MoveEnergyRequirement,
    ProfilePicture,
    Rarity,
)

admin.site.register(Ability)
admin.site.register(Card)
admin.site.register(CardType)
admin.site.register(CardStage)
admin.site.register(EnergyType)
admin.site.register(Move)
admin.site.register(MoveEnergyRequirement)
admin.site.register(Rarity)
admin.site.register(Collection)
admin.site.register(Illustrator)
admin.site.register(ProfilePicture)
