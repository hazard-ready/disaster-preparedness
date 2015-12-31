# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0020_auto_20150327_0300'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandslideDeformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('label', models.CharField(max_length=11)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=2991)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LiquefactionDeformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('label', models.CharField(max_length=11)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=2991)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
