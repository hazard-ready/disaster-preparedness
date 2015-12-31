# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0021_landslidedeformation_liquefactiondeformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='snugget',
            name='landslide_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='+', to='world.LandslideDeformation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snugget',
            name='liquifaction_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='+', to='world.LiquefactionDeformation'),
            preserve_default=True,
        ),
    ]
