from django.db import models
import timedelta

# Create your models here.


class Play(models.Model):
	
	game = models.ForeignKey('Game')
	period = models.PositiveSmallIntegerField()
	time = timedelta.fields.TimedeltaField()
	home_5 = models.ManyToManyField('Player', related_name='home_5')
	away_5 = models.ManyToManyField('Player', related_name='away_5')
	points = models.PositiveSmallIntegerField()
	team = models.ForeignKey('Team')

class Game(models.Model): 
	
	home_team = models.ForeignKey('Team', related_name = 'home_team')
	away_team = models.ForeignKey('Team', related_name = 'away_team')
	date = models.DateTimeField('Game date')
	
	def _score(self, team):
		points = 0
		for play in self.play_set.all():
			if play.team.name == team.name:
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
	 