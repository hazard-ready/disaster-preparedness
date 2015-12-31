# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0033_auto_20150328_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snugget',
            name='impact_zone_filter',
            field=models.ForeignKey(to='world.ImpactZone', related_name='+', on_delete=django.db.models.deletion.PROTECT, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='ImpactZoneData',
        ),
    ]
