from bets.models import Team, Score, Match, Player
from datetime import datetime, timezone
import requests

def load_teams():
    url = 'http://api.football-data.org/v1/competitions/467/teams'
    headers = {'X-Response-Control':'minified', 'X-Auth-Token' : 'a8ca8189a22d4b0e8c7f11da042f497a'}
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()
        for team in data['teams']:
            apiID = int(team['id'])
            name = team['name']
            crestUrl = team['crestUrl']
            team_query = Team.objects.filter(apiID=apiID)
            if team_query.exists():
                team_query.update(name=name, crestUrl=crestUrl)
            else:
                Team.objects.create(apiID=apiID, name=name, crestUrl=crestUrl)

def load_players():
    headers = {'X-Response-Control':'minified', 'X-Auth-Token' : 'a8ca8189a22d4b0e8c7f11da042f497a'}
    teams = Team.objects.all()
    for team in teams:
        url = 'http://api.football-data.org/v1/teams/' + str(team.apiID) + '/players'
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()
            for player in data['players']:
                name = player['name']
                position = player['position']
                player_query = Player.objects.filter(name=name, team=team, position=position)
                if not player_query.exists():
                    Player.objects.create(name=name, team=team, position=position)

def load_matches():
    url = 'http://api.football-data.org/v1/competitions/467/fixtures'
    headers = {'X-Response-Control':'minified', 'X-Auth-Token' : 'a8ca8189a22d4b0e8c7f11da042f497a'}
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()
        for fixture in data['fixtures']:
            match_as_dict = extract_match(fixture)
            match_query = Match.objects.filter(apiID=match_as_dict['apiID'])
            if match_query.exists():
                match_query.update(**match_as_dict)
            else:
                Match.objects.create(**match_as_dict)

def extract_match(fixture):
    apiID = int(fixture['id'])
    date = fixture['date']
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    date = date.replace(tzinfo=timezone.utc)
    homeTeamName = fixture['homeTeamName']
    awayTeamName = fixture['awayTeamName']
    try:
        homeTeam = Team.objects.get(name=homeTeamName)
    except:
        homeTeam = None
    try:
        awayTeam = Team.objects.get(name=awayTeamName)
    except:
        awayTeam = None
    result = fixture['result']
    try:
        home = int(result['goalsHomeTeam'])
        away = int(result['goalsAwayTeam'])
    except:
        home = None
        away = None
    score = Score.objects.create(home=home, away=away)
    return {'apiID': apiID, 'date': date, 'homeTeam': homeTeam, 'awayTeam': awayTeam, 'score': score}

def fake_data_load_matches():
    url = 'http://api.football-data.org/v1/competitions/467/fixtures'
    headers = {'X-Response-Control':'minified', 'X-Auth-Token' : 'a8ca8189a22d4b0e8c7f11da042f497a'}
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()
        for fixture in data['fixtures']:
            fixture['result']['goalsHomeTeam'] = "1"
            fixture['result']['goalsAwayTeam'] = "0"
            match_as_dict = extract_match(fixture)
            match_query = Match.objects.filter(apiID=match_as_dict['apiID'])
            if match_query.exists():
                match_query.update(**match_as_dict)
            else:
                Match.objects.create(**match_as_dict)
