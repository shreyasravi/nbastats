# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name=b'Game date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.PositiveSmallIntegerField()),
                ('time', models.TimeField()),
                ('points', models.PositiveSmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=3, choices=[(b'BRO', b'Brooklyn Nets'), (b'CHA', b'Charlotte Bobcats')])),
            ],
            options={
            },
            bases=(models.Model,),
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
            field=models.ManyToManyField(related_name='away_5', to='players.Player'),
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
            field=models.ManyToManyField(related_name='home_5', to='players.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='play',
            name='team',
            field=models.ForeignKey(to='players.Team'),
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
    ]
