import csv
from players import models





def import_game(filename):
	print(filename.split('_')[0],filename.split('_')[1],filename.split('_')[2])
	date = datetime(filename.split('_')[4],filename.split('_')[3],
					filename.split('_')[2])
	away_team, created = Team.objects.get_or_create(name=filename.split('_')[0])
	home_team, created = Team.objects.get_or_create(name=filename.split('_')[1])
	
	game, created = Game.objects.get_or_create(home_team=home_team, away_team=away_team,
									  date=date)
										
	input_file = csv.DictReader(open('C:\\Personal\\nbastats\\nbastats\\players\\data\\games_play-by-play\\'+filename))
	for row in input_file:
		a1, created = Player.objects.get_or_create(first_name=row['a1'].split()[0],
										  last_name=row['a1'].split()[1],
										  team=away_team)
		a2, created = Player.objects.get_or_create(first_name=row['a2'].split()[0],
										  last_name=row['a2'].split()[1],
										  team=away_team)
		a3, created = Player.objects.get_or_create(first_name=row['a3'].split()[0],
										  last_name=row['a3'].split()[1],
										  team=away_team)
		a4, created = Player.objects.get_or_create(first_name=row['a4'].split()[0],
										  last_name=row['a4'].split()[1],
										  team=away_team)
		a5, created = Player.objects.get_or_create(first_name=row['a5'].split()[0],
										  last_name=row['a5'].split()[1],
										  team=away_team) 
		h1, created = Player.objects.get_or_create(first_name=row['h1'].split()[0],
										  last_name=row['h1'].split()[1],
										  team=home_team)
		h2, created = Player.objects.get_or_create(first_name=row['h2'].split()[0],
										  last_name=row['h2'].split()[1],
										  team=home_team)
		h3, created = Player.objects.get_or_create(first_name=row['h3'].split()[0],
										  last_name=row['h3'].split()[1],
										  team=home_team)
		h4, created = Player.objects.get_or_create(first_name=row['h4'].split()[0],
										  last_name=row['h4'].split()[1],
										  team=home_team)
		h5, created = Player.objects.get_or_create(first_name=row['h5'].split()[0],
										  last_name=row['h5'].split()[1],
										  team=home_team)
		if row['team'] == away_team.name:
			team = away_team
		else: 
			team = home_team
		period=row['period']
		if row['points'] is None:
			points = 0
		else:
			points = row['points']
		time=datetime.strptime(row['time'], '%M:%S')
		play, created = Play.objects.get_or_create(game=game, team=team,
												   period=period,
												   time=time)
												   
filename = 'BRO_CHA_3_26_2014.csv'
import_game(filename)