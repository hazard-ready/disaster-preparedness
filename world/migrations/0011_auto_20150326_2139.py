# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0010_expectedgroundshaking'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImpactZoneData',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('area', models.IntegerField()),
                ('perimeter', models.IntegerField()),
                ('orbndy24', models.IntegerField()),
                ('orbndy24i', models.IntegerField()),
                ('subjstate', models.CharField(max_length=50)),
                ('feature', models.IntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='ImpactZone',
        ),
        migrations.AlterField(
            model_name='expectedgroundshaking',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=2991),
            preserve_default=True,
        ),
    ]
