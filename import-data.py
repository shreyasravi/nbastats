#import sys
#sys.path.append('C:\\Personal\\nbastats\\nbastats\\nbastats\\settings.py')
#sys.path.append('C:\\Personal\\nbastats\\nbastats\\nbastats')
#sys.path.append('C:\\Personal\\nbastats\\nbastats')
#print(sys.path)


import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'nbastats.settings'
import csv, datetime
from players import models
import django
django.setup()



def import_play(row, home_team, away_team, game):
		""""Imports one line of play-by-play csv data"""
		
		a1, created = models.Player.objects.get_or_create(first_name=row['a1'].split()[0].lower(),
										  last_name=row['a1'].split()[1].lower(),
										  team=away_team)
		a2, created = models.Player.objects.get_or_create(first_name=row['a2'].split()[0].lower(),
										  last_name=row['a2'].split()[1].lower(),
										  team=away_team)
		a3, created = models.Player.objects.get_or_create(first_name=row['a3'].split()[0].lower(),
										  last_name=row['a3'].split()[1].lower(),
										  team=away_team)
		a4, created = models.Player.objects.get_or_create(first_name=row['a4'].split()[0].lower(),
										  last_name=row['a4'].split()[1].lower(),
										  team=away_team)
		a5, created = models.Player.objects.get_or_create(first_name=row['a5'].split()[0].lower(),
										  last_name=row['a5'].split()[1].lower(),
										  team=away_team) 
		h1, created = models.Player.objects.get_or_create(first_name=row['h1'].split()[0].lower(),
										  last_name=row['h1'].split()[1].lower(),
										  team=home_team)
		h2, created = models.Player.objects.get_or_create(first_name=row['h2'].split()[0].lower(),
										  last_name=row['h2'].split()[1].lower(),
										  team=home_team)
		h3, created = models.Player.objects.get_or_create(first_name=row['h3'].split()[0].lower(),
										  last_name=row['h3'].split()[1].lower(),
										  team=home_team)
		h4, created = models.Player.objects.get_or_create(first_name=row['h4'].split()[0].lower(),
										  last_name=row['h4'].split()[1].lower(),
										  team=home_team)
		h5, created = models.Player.objects.get_or_create(first_name=row['h5'].split()[0].lower(),
										  last_name=row['h5'].split()[1].lower(),
										  team=home_team)
		period=row['period']
		minutes, seconds = int(row['time'].split(':')[0]), int(row['time'].split(':')[1])
		time = datetime.timedelta(minutes=minutes, seconds=seconds)
		ejected = None
		if row['etype'] == 'ejected':
			ejected = models.Player.objects.get(first_name=row['player'].split()[0].lower(),
										  last_name=row['player'].split()[1].lower())
		number = None
		if row['num']:
			number = row['num']
		etype = row['etype']
		player = None
		if row['player']:
			player = models.Player.objects.get(
									first_name=row['player'].split()[0].lower(),
									last_name=row['player'].split()[1].lower())
		play, created = models.Play.objects.get_or_create(game=game, time=time,
														  period=period, 
														  ejected=ejected,
														  number=number,
														  etype=etype,
														  player=player)
		play.home_5.add(h1, h2, h3, h4, h5)
		play.away_5.add(a1, a2, a3, a4, a5)
		play.save()
		print(play.pk, play.period, play.home_5.all())
		# Handling a shot instance
		if row['etype'] == 'shot' or row['etype'] == 'free throw':
			shot_type = {'free throw':'FT', 'jump':'J', 
						 'driving layup':'DL', '3pt':'3pt shot', 
					     'pullup jump':'PJ', 'layup':'L',
						 'dunk':'D', 'shot':'S', 'running':'R', 'tip':'T'}
			if row['etype'] == 'free throw':
				type = shot_type[row['etype']]
			else:
				type = shot_type[row['type']]
			result = row['result']
			x, y = None, None
			if row['x']:
				x, y = row['x'], row['y']
			shooter = models.Player.objects.get(
										  first_name=row['player'].split()[0].lower(),
										  last_name=row['player'].split()[1].lower())
			assist = None
			if row['assist']:
				assist = models.Player.objects.get(
										  first_name=row['assist'].split()[0].lower(),
										  last_name=row['assist'].split()[1].lower())
			block = None
			if row['block']:
				block = models.Player.objects.get(
										  first_name=row['block'].split()[0].lower(),
										  last_name=row['block'].split()[1].lower())
			points = 0
			if row['points']:
				points = row['points']
			else: 
				if 'free throw' == row['etype'] and 'made' == row['result']:
					points = 1
			shot, created = models.Shot.objects.get_or_create(result=result,
												type=type, x=x, y=y, 
												shooter=shooter, assist=assist,
												block=block, team=shooter.team,
												play=play, points=points)
												
			shot.save()
		# Handling a foul instance
		if row['etype'] == 'foul':
			foul_type = {'personal':'P', 'shooting':'S', 'offensive':'O',
						  'loose ball':'LB', 'flagrant':'F'}
			type = foul_type[row['type']]
			fouler = models.Player.objects.get(
										  first_name=row['player'].split()[0].lower(),
										  last_name=row['player'].split()[1].lower())
			fouled = models.Player.objects.get(
										  first_name=row['opponent'].split()[0].lower(),
										  last_name=row['opponent'].split()[1].lower())
			foul, created = models.Foul.objects.get_or_create(type=type,
										  fouler=fouler, fouled=fouled,
										  play=play, team=fouler.team)
			foul.save()
		# Handling a turnover instance
		if row['etype'] == 'turnover':
			turnover_type = {'bad pass':'BP', 'lost ball':'LB', 
						'kickball violation':'KV',
						'steps out of bounds':'OB', 
						'traveling':'T', 'lost ball':'LB'}
			type = None
			if row['reason']:
				type = turnover_type[row['reason']]
			committed = None
			if row['player']:
				committed = models.Player.objects.get(
										  first_name=row['player'].split()[0].lower(),
										  last_name=row['player'].split()[1].lower())
			steal = None
			if row['steal']:
				steal = models.Player.objects.get(
										  first_name=row['steal'].split()[0].lower(),
										  last_name=row['steal'].split()[1].lower())
			team = models.Team.objects.get(name=row['team'])
			turnover, created = models.Turnover.objects.get_or_create(type=type,
										  committed=committed, steal=steal,
										  play=play, team=team)
			turnover.save()
		if row['etype'] == 'rebound':
			type = row['type']
			player = None
			if row['player']:
				player = models.Player.objects.get(
										  first_name=row['player'].split()[0].lower(),
										  last_name=row['player'].split()[1].lower())
			team = models.Team.objects.get(name=row['team'])
			rebound, created = models.Rebound.objects.get_or_create(type=type,
										  player=player, team=team, play=play)
			rebound.save()
		if row['etype'] == 'jump ball':
			home = models.Player.objects.get(
										  first_name=row['home'].split()[0].lower(),
										  last_name=row['home'].split()[1].lower())
			away = models.Player.objects.get(
										  first_name=row['away'].split()[0].lower(),
										  last_name=row['away'].split()[1].lower())
			possession = models.Player.objects.get(
										  first_name=row['possession'].split()[0].lower(),
										  last_name=row['possession'].split()[1].lower())
			jumpball, created = models.Jumpball.objects.get_or_create(home=home,
														away=away, play=play,
														possession=possession)



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
		import_play(row, home_team, away_team, game)

filename = 'BRO_CHA_3_26_2014.csv'
import_game(filename)