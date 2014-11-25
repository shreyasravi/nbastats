# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timedelta.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foul',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=2, choices=[('P', 'Personal'), ('S', 'Shooting'), ('O', 'Offensive'), ('LB', 'Loose Ball'), ('F', 'Flagrant')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Game date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Jumpball',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.PositiveSmallIntegerField()),
                ('time', timedelta.fields.TimedeltaField(min_value=None, max_value=None)),
                ('number', models.PositiveSmallIntegerField(null=True)),
                ('etype', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rebound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=3, choices=[('def', 'Defensive'), ('off', 'Offensive')])),
                ('play', models.OneToOneField(to='players.Play')),
                ('player', models.ForeignKey(null=True, to='players.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.BooleanField()),
                ('type', models.CharField(max_length=2, choices=[('FT', 'Free Throw'), ('J', 'Jump Shot'), ('DL', 'Driving Layup'), ('3p', '3pt Shot'), ('PJ', 'Pullup Jumper'), ('L', 'Layup'), ('D', 'Dunk'), ('S', 'Shot')])),
                ('x', models.PositiveSmallIntegerField(null=True)),
                ('y', models.PositiveSmallIntegerField(null=True)),
                ('points', models.PositiveSmallIntegerField()),
                ('assist', models.ForeignKey(to='players.Player', related_name='assist', null=True)),
                ('block', models.ForeignKey(to='players.Player', related_name='block', null=True)),
                ('play', models.OneToOneField(to='players.Play')),
                ('shooter', models.ForeignKey(related_name='shooter', to='players.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3, choices=[('BRO', 'Brooklyn Nets'), ('CHA', 'Charlotte Bobcats')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Turnover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(null=True, max_length=2, choices=[('BP', 'Bad Pass'), ('LB', 'Lost Ball'), ('KV', 'Kickball Violation'), ('OB', 'Steps Out of Bounds'), ('T', 'Travelling'), ('LB', 'Lost Ball')])),
                ('committed', models.ForeignKey(to='players.Player', related_name='committed', null=True)),
                ('play', models.OneToOneField(to='players.Play')),
                ('steal', models.ForeignKey(to='players.Player', related_name='steal', null=True)),
                ('team', models.ForeignKey(to='players.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='shot',
            name='team',
            field=models.ForeignKey(to='players.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rebound',
            name='team',
            field=models.ForeignKey(to='players.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(to='players.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='play',
            name='away_5',
            field=models.ManyToManyField(to='players.Player', related_name='away_5'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='play',
            name='ejected',
            field=models.ForeignKey(to='players.Player', related_name='ejected', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='play',
            name='game',
            field=models.ForeignKey(to='players.Game'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='play',
            name='home_5',
            field=models.ManyToManyField(to='players.Player', related_name='home_5'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='play',
            name='player',
            field=models.ForeignKey(to='players.Player', related_name='player', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jumpball',
            name='away',
            field=models.ForeignKey(related_name='away', to='players.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jumpball',
            name='home',
            field=models.ForeignKey(related_name='home', to='players.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jumpball',
            name='play',
            field=models.OneToOneField(to='players.Play'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jumpball',
            name='possession',
            field=models.ForeignKey(related_name='possession', to='players.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='away_team',
            field=models.ForeignKey(related_name='away_team', to='players.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(related_name='home_team', to='players.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foul',
            name='fouled',
            field=models.ForeignKey(related_name='fouled', to='players.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foul',
            name='fouler',
            field=models.ForeignKey(related_name='fouler', to='players.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foul',
            name='play',
            field=models.OneToOneField(to='players.Play'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foul',
            name='team',
            field=models.ForeignKey(to='players.Team'),
            preserve_default=True,
        ),
    ]
