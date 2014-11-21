# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timedelta.fields


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='play',
            name=b'time',
            field=timedelta.fields.TimedeltaField(max_value=None, min_value=None),
            preserve_default=True,
        ),
    ]
