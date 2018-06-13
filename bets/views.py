from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Match, Team, Bet1X2, Group, Player, GoalKingBet, Gambler, BestThree

def index(request):
    template = 'bets/index.html'
    context = {}
    return render(request, template, context)

@login_required(login_url='/login')
def lohkovaihe(request):
    user = request.user
    if request.method == 'POST' and hasattr(user, 'gambler'):
        gambler = user.gambler
        for match in Match.objects.all()[:48]:
            match = match
            bet = request.POST.get(str(match.id))
            if gambler.bet1x2_set.filter(match=match).exists():
                gambler.bet1x2_set.filter(match=match).update(bet=bet)
            else:
                Bet1X2.objects.create(match=match, bet=bet, gambler=gambler) 
        template = 'bets/ok.html'
        return render(request, template, {'user': request.user})
    else:
        template = 'bets/lohkovaihe.html'
        groups = Group.objects.all()
        context = {'groups': groups, 'user': request.user}
        return render(request, template, context)

@login_required(login_url='/login')
def maalikuningas(request):
    user = request.user
    if request.method == 'POST' and hasattr(user, 'gambler'):
        gambler = user.gambler
        player = get_object_or_404(Player, id=request.POST.get('maalikuningas'))
        if gambler.goalkingbet_set.all().exists():
            gambler.goalkingbet_set.all().update(goalKing=player)
        else:
            GoalKingBet.objects.create(gambler=gambler, goalKing=player)
        template = 'bets/ok.html'
        return render(request, template, {'user': request.user})
    else:
        template = 'bets/maalikuningas.html'
        players = Player.objects.all()
        context = {'players': players, 'user': request.user}
        return render(request, template, context)

@login_required(login_url='/login')
def kolmikko(request):
    user = request.user
    if request.method == 'POST' and hasattr(user, 'gambler'):
        gambler = user.gambler
        first = get_object_or_404(Team, id=request.POST.get('voittaja'))
        second = get_object_or_404(Team, id=request.POST.get('toinen'))
        third = get_object_or_404(Team, id=request.POST.get('kolmas'))
        if gambler.bestthree_set.all().exists():
            gambler.bestthree_set.all().update(first=first, second=second, third=third)
        else:
            BestThree.objects.create(gambler=gambler, first=first, second=second, third=third)
        template = 'bets/ok.html'
        return render(request, template, {'user': request.user})
    else:
        template = 'bets/kolmikko.html'
        teams = Team.objects.all()
        context = {'teams': teams, 'user': request.user}
        return render(request, template, context)

@login_required(login_url='/login')
def vertaile(request):
    template = 'bets/vertaile.html'
    matches = Match.objects.all()[:48]
    lohko = Bet1X2.objects.all()
    kuningas = GoalKingBet.objects.all()
    kolmikko = BestThree.objects.all()
    context = {'matches': matches, 'lohko': lohko, 'kuningas': kuningas, 'kolmikko': kolmikko, 'user': request.user}
    return render(request, template, context)

def tilanne(request):
    template = 'bets/tilanne.html'
    gamblers = Gambler.objects.all()
    sorted_gamblers = sorted(gamblers, key=lambda obj: obj.getPoints(), reverse=True)
    context = {'gamblers': sorted_gamblers, 'user': request.user}
    return render(request, template, context)
