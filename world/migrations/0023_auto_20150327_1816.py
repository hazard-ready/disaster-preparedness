# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0022_auto_20150327_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectedgroundshaking',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landslidedeformation',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='liquefactiondeformation',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992),
            preserve_default=True,
        ),
    ]
