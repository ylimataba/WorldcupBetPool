from django.contrib import admin
from .models import Team, Match, Bet1X2, Group, GoalKingBet, Gambler

admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Bet1X2)
admin.site.register(Group)
admin.site.register(GoalKingBet)
admin.site.register(Gambler)