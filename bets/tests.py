from django.test import TestCase
from django.contrib.auth.models import User
from bets.models import Team, Score, Match, Player, BetScore, Bet1X2
from datetime import datetime, timezone
from bets.database import *

class BetTestCase(TestCase):
    def setUp(self):
        homeTeam = Team.objects.create(apiID=808, name="Russia",crestUrl="https://upload.wikimedia.org/wikipedia/commons/f/f3/Flag_of_Russia.svg")
        awayTeam = Team.objects.create(apiID=801, name="Saudi Arabia", crestUrl="https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg")
        score1 = Score.objects.create(home=0, away=0)
        score2 = Score.objects.create(home=1, away=0)
        date = datetime.strptime("2018-06-14T15:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        date = date.replace(tzinfo=timezone.utc)
        match = Match.objects.create(apiID=1, date=date, homeTeam=homeTeam, awayTeam=awayTeam, score=score1)
        user1 = User.objects.create_user(username='user1', password='12345')
        user2 = User.objects.create_user(username='user2', password='12345')
        BetScore.objects.create(match=match, score=score1, user=user1)
        BetScore.objects.create(match=match, score=score2, user=user2)
        Bet1X2.objects.create(match=match, bet='X', user=user1)
        Bet1X2.objects.create(match=match, bet='1', user=user2)

    def test_score_bet(self):
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        bet1 = BetScore.objects.get(user=user1)
        bet2 = BetScore.objects.get(user=user2)
        self.assertEquals(bet1.getPoints(1),1)
        self.assertEquals(bet2.getPoints(1),0)

    def test_bet1X2(self):
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        bet1 = Bet1X2.objects.get(user=user1)
        bet2 = Bet1X2.objects.get(user=user2)
        self.assertEquals(bet1.getPoints(1),1)
        self.assertEquals(bet2.getPoints(1),0)

class RequestTestCase(TestCase):
    def setUp(self):
        load_teams()

    def test_load_teams(self):
        load_teams()
        teams = Team.objects.all()
        self.assertEquals(len(teams), 32)

    def test_load_matches(self):
        load_matches()
        matches = Match.objects.all()
        self.assertEquals(len(matches),64)

    def test_fake_data_load_matches(self):
        load_matches()
        fake_data_load_matches()
        matches = Match.objects.all()
        self.assertEquals(len(matches),64)

    def test_load_players(self):
        load_players()
        players = Player.objects.all()
        for player in players:
            print(player)

class TeamTestCase(TestCase):
    def setUp(self):
        load_teams()

    def test_get_matches(self):
        load_matches()
        russia = Team.objects.get(name="Russia")
        matches = russia.getMatches()
        for match in matches:
            print(match)
    
    def test_get_goals(self):
        fake_data_load_matches()
        russia = Team.objects.get(name="Russia")
        print(russia.getGoals())

    def test_get_points(self):
        fake_data_load_matches()
        russia = Team.objects.get(name="Russia")
        print(russia.getPoints())
        
