# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0034_auto_20150328_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImpactZoneData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.CharField(max_length=10)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='snugget',
            name='impact_zone_filter',
            field=models.ForeignKey(to='world.ImpactZoneData', related_name='+', null=True, on_delete=django.db.models.deletion.PROTECT, blank=True),
            preserve_default=True,
        ),
    ]
