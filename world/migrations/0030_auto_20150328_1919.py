# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0029_auto_20150328_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snugget',
            name='impact_zone_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='world.ImpactZoneData', null=True, blank=True, related_name='+'),
            preserve_default=True,
        ),
    ]
