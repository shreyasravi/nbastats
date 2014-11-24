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
			if play.team.name == team.name:
				print(play.points, play.period)
				points = points + play.points
		return points
	
	def away_score(self):
		return self._score(self.away_team)

	def home_score(self):
		return self._score(self.home_team)
		
class Player(models.Model):
	
	first_name = models.CharField(max_length=15)
	last_name = models.CharField(max_length=15)
	team = models.ForeignKey('Team')
	
class Team(models.Model):
	TEAM_CHOICES = (('BRO', 'Brooklyn Nets'), ('CHA', 'Charlotte Bobcats'))
	name = models.CharField(max_length=3, choices=TEAM_CHOICES)
	 