from django.db import models
import timedelta

class Play(models.Model):
	
	game = models.ForeignKey('Game')
	period = models.PositiveSmallIntegerField()
	time = timedelta.fields.TimedeltaField()
	home_5 = models.ManyToManyField('Player', related_name='home_5')
	away_5 = models.ManyToManyField('Player', related_name='away_5')
	ejected = models.ForeignKey('Player', related_name='ejected', null=True)
	# For free throws: ensures that we get a unique play for each line of the csv
	number = models.PositiveSmallIntegerField(null=True)
	etype = models.CharField(max_length=30) # Ensure we get unique plays
	player = models.ForeignKey('Player', related_name='player', null=True)

class Shot(models.Model):
	
	SHOT_CHOICES = (('FT', 'Free Throw'),('J', 'Jump Shot'), ('DL', 'Driving Layup'),
					('3p', '3pt Shot'), ('PJ', 'Pullup Jumper'), ('L', 'Layup'),
					('D', 'Dunk'), ('S', 'Shot'), ('R', 'Running'), ('T', 'Tip'))
	result = models.BooleanField() # True = made, False = missed
	type = models.CharField(max_length=2, choices=SHOT_CHOICES)
	x = models.PositiveSmallIntegerField(null=True) # null=True for free throws
	y = models.PositiveSmallIntegerField(null=True)
	shooter = models.ForeignKey('Player', related_name='shooter')
	assist = models.ForeignKey('Player', related_name='assist', null=True)
	block = models.ForeignKey('Player', related_name='block', null=True)
	play = models.OneToOneField('Play')
	points = models.PositiveSmallIntegerField()
	team = models.ForeignKey('Team')

class Foul(models.Model):

	FOUL_CHOICES = (('P', 'Personal'), ('S', 'Shooting'), ('O', 'Offensive'),
					('LB', 'Loose Ball'), ('F', 'Flagrant'))
					
	fouler = models.ForeignKey('Player', related_name='fouler')
	fouled = models.ForeignKey('Player', related_name='fouled')
	play = models.OneToOneField('Play')
	team = models.ForeignKey('Team')
	type = models.CharField(max_length=2, choices=FOUL_CHOICES)
	
class Turnover(models.Model):
	
	TURNOVER_CHOICES = (('BP', 'Bad Pass'), ('LB', 'Lost Ball'), 
						('KV', 'Kickball Violation'),
						('OB', 'Steps Out of Bounds'), 
						('T', 'Travelling'), ('LB', 'Lost Ball'))
					
	# Occassionally, a turnover is not charged to a player, hence null=True
	committed = models.ForeignKey('Player', related_name='committed', null=True)
	steal = models.ForeignKey('Player', related_name='steal', null=True)
	type = models.CharField(max_length=2, choices=TURNOVER_CHOICES, null=True)
	team = models.ForeignKey('Team')
	play = models.OneToOneField('Play')

class Rebound(models.Model):
	
	REBOUND_CHOICES = (('def', 'Defensive'), ('off', 'Offensive'))
	player = models.ForeignKey('Player', null=True)
	type = models.CharField(max_length=3, choices=REBOUND_CHOICES)
	team = models.ForeignKey('Team')
	play = models.OneToOneField('Play')

class Jumpball(models.Model):

	home = models.ForeignKey('Player', related_name='home')
	away = models.ForeignKey('Player', related_name='away')
	possession = models.ForeignKey('Player', related_name='possession')
	play = models.OneToOneField('Play')
	
class Game(models.Model): 
	
	home_team = models.ForeignKey('Team', related_name = 'home_team')
	away_team = models.ForeignKey('Team', related_name = 'away_team')
	date = models.DateTimeField('Game date')
	
	def _score(self, team):
		points = 0
		for play in self.play_set.all():
			if hasattr(play, 'shot') == True:
				if play.shot.team == team:
					points = points + play.shot.points
		return points
	
	def away_score(self):
		return self._score(self.away_team)

	def home_score(self):
		return self._score(self.home_team)
	
	def __str__(self):
		return '%s @ %s, %s' % (self.away_team, self.home_team, self.date.date())
		
class Player(models.Model):
	
	first_name = models.CharField(max_length=15)
	last_name = models.CharField(max_length=15)
	team = models.ForeignKey('Team')
	
	def plus_minus(self, games, teammates=None, opponents=None):
		differential = 0
		for game in games:
			for play in game.play_set.all():
				if self in play.away_5.all() or self in play.home_5.all():
					if hasattr(play,'shot') == True:
						if play.shot.team == self.team:
							differential = differential + play.shot.points
						else:
							differential = differential - play.shot.points
				#		print(play.shot.points, differential, play.shot.type)
		return differential
	
	def ppg(self, games=None):
		points = 0
		if games:
			games = games
		else:
			games = Game.objects.all()
		for game in games:
			for shot in self.shooter.filter(play__game=game):
				points = shot.points + points
		return points
	
	def apg(self, games=None):
		assists = 0
		if games:
			games = games
		else:
			games = Game.objects.all()
		for game in games:
			for assist in self.assist.filter(play__game=game):
				assists += 1
		return assists
		
	def spg(self, games=None):
		steals = 0
		if games:
			games = games
		else:
			games = Game.objects.all()
		for game in games:
			for steal in self.steal.filter(play__game=game):
				steals += 1
		return steals
	


	def __str__(self):
		return '%s %s' % (self.first_name, self.last_name)
	
	
	
class Team(models.Model):
	TEAM_CHOICES = (('BRO', 'Brooklyn Nets'), ('CHA', 'Charlotte Bobcats'))
	name = models.CharField(max_length=3, choices=TEAM_CHOICES)
	def __str__(self):
		return '%s' % (self.get_name_display())
	 