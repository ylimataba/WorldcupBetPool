from django.db import models
from django.contrib.auth.models import User


factors = {'lohko': 1, 'kuningas': 10, 'kolmikko': 10, 'tulos': 3}
results = {'kuningas': None, 'voittaja': None, 'toinen': None, 'kolmas': None}

class Group(models.Model):
    name = models.CharField(max_length=10)

    def getMatches(self):
        matches = Match.objects.none()
        for team in self.team_set.all():
            matches = matches | team.getMatches()
        return matches[:6]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Team(models.Model):
    apiID = models.PositiveIntegerField()
    name = models.CharField(max_length=48)
    crestUrl = models.URLField(max_length=200, null=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)
    
    def getMatches(self):
        matches = self.homeMatch.all()
        matches = matches | self.awayMatch.all()
        return matches
    
    def getGoals(self):
        made = 0
        against = 0
        for match in self.getMatches():
            if self is match.homeTeam:
                made += match.score.home
                against += match.score.away
            else:
                made += match.score.away
                against += match.score.home
        return {'made': made, 'against': against}

    def getPoints(self):
        points = 0
        for match in self.getMatches():
            result = match.get1X2()
            if result == 'X':
                points += 1
            elif result == '1' and self is match.homeTeam:
                points += 3
            elif result == '2' and self is match.awayTeam:
                points += 3
        return points

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=48)
    position = models.CharField(max_length=48)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    goals = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["team", "name"]
    
    def __str__(self):
        string = "{0} {1} {2}".format(self.team.name, self.name, self.position)
        return string
    

class Score(models.Model):
    home = models.PositiveIntegerField(null=True)
    away = models.PositiveIntegerField(null=True)

class Match(models.Model):
    apiID = models.PositiveIntegerField()
    date = models.DateTimeField()
    homeTeam = models.ForeignKey("Team", related_name="homeMatch", on_delete=models.CASCADE, null=True)
    awayTeam = models.ForeignKey("Team", related_name="awayMatch", on_delete=models.CASCADE, null=True)
    score = models.ForeignKey("Score", on_delete=models.CASCADE)
    
    def hasScore(self):
        if self.score.home is not None and self.score.away is not None:
            return True
        return False

    def get1X2(self):
        if self.hasScore():
            if self.score.home == self.score.away:
                return 'X'
            elif self.score.home > self.score.away:
                return '1'
            else:
                return '2'
        return None

    class Meta:
        ordering = ["date"]

    def __str__(self):
        home = None
        away = None
        if self.homeTeam:
            home = self.homeTeam.name
        if self.awayTeam:
            away = self.awayTeam.name
        string = "{0}: {1} {2}-{3} {4}".format(self.date, home, self.score.home, self.score.away, away)
        return string

class Gambler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def getPoints(self):
        points = 0
        for bet in self.bet1x2_set.all():
            points += bet.getPoints()
        for bet in self.goalkingbet_set.all():
            points += bet.getPoints()
        for bet in self.bestthree_set.all():
            points += bet.getPoints()
        for bet in self.betscore_set.all():
            points += bet.getPoints()
        return points

    class Meta:
        ordering = ["user.username"]

    def __str__(self):
        return self.user.username

class BetScore(models.Model):
    match = models.ForeignKey("Match", on_delete=models.CASCADE)
    score = models.ForeignKey("Score", on_delete=models.CASCADE)
    gambler = models.ForeignKey(Gambler, on_delete=models.CASCADE)
    
    def getPoints(self):
        if self.match.hasScore():
            if self.score.away == self.match.score.away and self.score.home == self.match.score.home:
                return factors['tulos']
        return 0

    class Meta:
        ordering = ["match", "gambler"]

class Bet1X2(models.Model):
    match = models.ForeignKey("Match", on_delete=models.CASCADE)
    bet = models.CharField(max_length=1)
    gambler = models.ForeignKey(Gambler, on_delete=models.CASCADE)

    def getPoints(self):
        if self.match.get1X2() == self.bet:
            return factors['lohko']
        return 0

    class Meta:
        ordering = ["match", "gambler"]

    def __str__(self):
        string = "{0} {1} {2}".format(self.match, self.gambler.user, self.bet)
        return string

class GoalKingBet(models.Model):
    goalKing = models.ForeignKey("Player", on_delete=models.CASCADE)
    gambler = models.ForeignKey(Gambler, on_delete=models.CASCADE)

    def getPoints(self):
        if self.goalKing == results['kuningas']:
            return factors['kuningas']
        return 0

    class Meta:
        ordering = ["gambler"]

    def __str__(self):
        string = "{0} {1}".format(self.gambler.user.username, self.goalKing.name)
        return string

class BestThree(models.Model):
    first = models.ForeignKey("Team", related_name="first", on_delete=models.CASCADE)
    second = models.ForeignKey("Team", related_name="second", on_delete=models.CASCADE)
    third = models.ForeignKey("Team", related_name="third", on_delete=models.CASCADE)
    gambler = models.ForeignKey(Gambler, on_delete=models.CASCADE)

    def getPoints(self):
        return 0

    class Meta:
        ordering = ["gambler"]

    def __str__(self):
        return self.gambler.user.name
