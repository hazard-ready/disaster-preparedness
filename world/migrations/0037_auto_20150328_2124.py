# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0036_auto_20150328_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snugget',
            name='impact_zone_filter',
            field=models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.PROTECT, blank=True, to='world.ImpactZone'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='ImpactZoneData',
        ),
    ]
