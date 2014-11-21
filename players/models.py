from django.db import models
import timedelta

class Play(models.Model):
	
	game = models.ForeignKey('Game')
	period = models.PositiveSmallIntegerField()
	time = timedelta.fields.TimedeltaField()
	home_5 = models.ManyToManyField('Player', related_name='home_5')
	away_5 = models.ManyToManyField('Player', related_name='away_5')
	points = models.PositiveSmallIntegerField()
	team = models.ForeignKey('Team')
	number = models.PositiveSmallIntegerField(null=True) # For free throws 
	shot = models.ForeignKey('Shot', null=True) #There may not be a shot on the play

class Shot(models.Model):
	
	SHOT_CHOICES = (('FT', 'Free Throw'),('J', 'Jump Shot'), ('DL', 'Driving Layup')
					('3p', '3pt Shot'), ('PJ', 'Pullup Jumper'), ('L', 'Layup')
					('D', 'Dunk'), ('S', 'Shot'))
	result = models.BooleanField() # True = made, False = missed
	type = models.CharField(max_length = 2, choices = SHOT_CHOICES)
	x = models.PositiveSmallIntegerField()
	y = models.PositiveSmallIntegerField()
	shooter = models.ForeignKey('Player', related_name='shooter')
	assist = models.ForeignKey('Player', related_name='assist', null=True)
	block = models.ForeignKey('Player', related_name='block', null=True)

class Foul(models.Model):
	FOUL_CHOICES = (('P', 'Personal'), ('S', 'Shooting'), ('O', 'Offensive'),
					('LB', 'Loose Ball'), ('F', 'Flagrant'))
					
	fouler = models.ForeignKey('Player', related_name='fouler')
	fouled = models.ForeignKey('Player', related_name='fouled')
	
class Turnover(models.Model):
	TURNOVER_CHOICES = (('BP', 'Bad Pass', ('LB', 'Lost Ball'), 
						('KV', 'Kickball Violation'),
						('OB', 'Steps Out of Bounds'), 
						('T', 'Travelling'), ('LB', 'Lost Ball'))
					
	fouler = models.ForeignKey('Player', related_name='fouler')
	fouled = models.ForeignKey('Player', related_name='fouled')
	


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
	 