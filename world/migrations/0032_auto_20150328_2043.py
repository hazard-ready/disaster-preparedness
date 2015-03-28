# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0031_auto_20150328_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impactzonedata',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992),
            preserve_default=True,
        ),
    ]
