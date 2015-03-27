# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0017_auto_20150327_0255'),
    ]

    operations = [
        migrations.AddField(
            model_name='snugget',
            name='impact_zone_filter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='world.ImpactZone'),
            preserve_default=False,
        ),
    ]
