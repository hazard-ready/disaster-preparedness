# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0039_auto_20150328_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impactzonedata',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=2994),
            preserve_default=True,
        ),
    ]
