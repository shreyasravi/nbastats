# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shot',
            name='type',
            field=models.CharField(choices=[('FT', 'Free Throw'), ('J', 'Jump Shot'), ('DL', 'Driving Layup'), ('3p', '3pt Shot'), ('PJ', 'Pullup Jumper'), ('L', 'Layup'), ('D', 'Dunk'), ('S', 'Shot'), ('R', 'Running')], max_length=2),
            preserve_default=True,
        ),
    ]
