# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0009_delete_worldborder'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpectedGroundShaking',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('rate', models.IntegerField()),
                ('shaking', models.CharField(max_length=11)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=-1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
