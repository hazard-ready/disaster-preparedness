# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0019_auto_20150327_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snugget',
            name='impact_zone_filter',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, blank=True, to='world.ImpactZone', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='snugget',
            name='shaking_filter',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, blank=True, to='world.ExpectedGroundShaking', null=True),
            preserve_default=True,
        ),
    ]
