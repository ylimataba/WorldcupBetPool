# WorldcupBetPool
Website for our family to place bets on World Cup 2018 and compete against each other to see who's the best.

database.py utilizes https://www.football-data.org API to load information about teams, players and matches.

Matches can be updated with `python manage.py loadmatches`
I used heroku scheduler to run that command every 10 minutes for automatic score update.

The site has lot to improve performance wise but it works. I'm planning on improving it before Euro 2020.
