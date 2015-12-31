# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0037_auto_20150328_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImpactZoneData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('zone', models.CharField(max_length=10)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
