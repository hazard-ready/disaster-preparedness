# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0023_auto_20150327_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='snugget',
            name='tsunami_filter',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, null=True, blank=True, to='world.TsunamiZone'),
            preserve_default=True,
        ),
    ]
