# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0018_snugget_impact_zone_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snugget',
            name='impact_zone_filter',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='world.ImpactZone', related_name='+'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='snugget',
            name='shaking_filter',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='world.ExpectedGroundShaking', related_name='+'),
            preserve_default=True,
        ),
    ]
