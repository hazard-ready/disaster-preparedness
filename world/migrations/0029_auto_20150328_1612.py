# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0028_auto_20150328_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snugget',
            name='impact_zone_filter',
            field=models.ForeignKey(null=True, blank=True, related_name='+', on_delete=django.db.models.deletion.PROTECT, to='world.ImpactZoneData'),
            preserve_default=True,
        ),
    ]
