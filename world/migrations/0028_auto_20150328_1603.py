# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0027_auto_20150328_0251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impactzonedata',
            name='area',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='feature',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='orbndy24',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='orbndy24i',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='perimeter',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='subjstate',
        ),
        migrations.AddField(
            model_name='impactzonedata',
            name='zone',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='impactzonedata',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992),
            preserve_default=True,
        ),
    ]
