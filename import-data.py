import csv, datetime
from players import models
import django




django.setup()

def import_game(filename):
	year, month, day = int(filename.split('_')[4].split('.')[0]),int(filename.split('_')[2]),\
					   int(filename.split('_')[3])
	print(year, month, day)
	date = datetime.datetime(year,month,day)
	away_team, created = models.Team.objects.get_or_create(name=filename.split('_')[0])
	home_team, created = models.Team.objects.get_or_create(name=filename.split('_')[1])
	
	game, created = models.Game.objects.get_or_create(home_team=home_team, away_team=away_team,
									  date=date)
										
	input_file = csv.DictReader(open('C:\\Personal\\nbastats\\nbastats\\players\\data\\games_play-by-play\\'+filename))
	for row in input_file:
		a1, created = models.Player.objects.get_or_create(first_name=row['a1'].split()[0],
										  last_name=row['a1'].split()[1],
										  team=away_team)
		a2, created = models.Player.objects.get_or_create(first_name=row['a2'].split()[0],
										  last_name=row['a2'].split()[1],
										  team=away_team)
		a3, created = models.Player.objects.get_or_create(first_name=row['a3'].split()[0],
										  last_name=row['a3'].split()[1],
										  team=away_team)
		a4, created = models.Player.objects.get_or_create(first_name=row['a4'].split()[0],
										  last_name=row['a4'].split()[1],
										  team=away_team)
		a5, created = models.Player.objects.get_or_create(first_name=row['a5'].split()[0],
										  last_name=row['a5'].split()[1],
										  team=away_team) 
		h1, created = models.Player.objects.get_or_create(first_name=row['h1'].split()[0],
										  last_name=row['h1'].split()[1],
										  team=home_team)
		h2, created = models.Player.objects.get_or_create(first_name=row['h2'].split()[0],
										  last_name=row['h2'].split()[1],
										  team=home_team)
		h3, created = models.Player.objects.get_or_create(first_name=row['h3'].split()[0],
										  last_name=row['h3'].split()[1],
										  team=home_team)
		h4, created = models.Player.objects.get_or_create(first_name=row['h4'].split()[0],
										  last_name=row['h4'].split()[1],
										  team=home_team)
		h5, created = models.Player.objects.get_or_create(first_name=row['h5'].split()[0],
										  last_name=row['h5'].split()[1],
										  team=home_team)
		if row['team'] == away_team.name:
			team = away_team
		else: 
			team = home_team
		period=row['period']
		if row['points']:
			points = row['points']
		else: 
			if 'free throw' == row['etype'] and 'made' == row['result']:
				points = 1
			else:
				points = 0
		minutes, seconds = int(row['time'].split(':')[0]), int(row['time'].split(':')[1])
		if row['num']:
			number=row['num']
		else:
			number = None
		play, created = models.Play.objects.get_or_create(game=game, team=team,
												   period=period, points=points,
												   time=datetime.timedelta(
																minutes=minutes, 
																seconds=seconds),
												   number=number)
		play.home_5.add(h1, h2, h3, h4, h5)
		play.away_5.add(a1, a2, a3, a4, a5)
		play.save()
												   

filename = 'BRO_CHA_3_26_2014.csv'
import_game(filename)