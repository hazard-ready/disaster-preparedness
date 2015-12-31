# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0003_tsunamizone_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImpactZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.IntegerField()),
                ('perimeter', models.IntegerField()),
                ('orbndy24', models.IntegerField()),
                ('orbndy24i', models.IntegerField()),
                ('subjstate', models.CharField(max_length=50)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImpactZoneClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='impactzone',
            name='feature',
            field=models.ForeignKey(to='world.ImpactZoneClass'),
            preserve_default=True,
        ),
    ]
