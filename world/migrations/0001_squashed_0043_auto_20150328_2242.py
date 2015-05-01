# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    replaces = [('world', '0001_initial'), ('world', '0002_tsunamizone'), ('world', '0003_tsunamizone_name'), ('world', '0004_auto_20150324_2027'), ('world', '0005_auto_20150324_2057'), ('world', '0006_auto_20150324_2109'), ('world', '0007_auto_20150324_2138'), ('world', '0008_auto_20150325_2213'), ('world', '0009_delete_worldborder'), ('world', '0010_expectedgroundshaking'), ('world', '0011_auto_20150326_2139'), ('world', '0012_auto_20150326_2140'), ('world', '0013_auto_20150326_2151'), ('world', '0014_auto_20150326_2153'), ('world', '0015_infrastructurecategory_zone'), ('world', '0016_auto_20150327_0231'), ('world', '0017_auto_20150327_0255'), ('world', '0018_snugget_impact_zone_filter'), ('world', '0019_auto_20150327_0259'), ('world', '0020_auto_20150327_0300'), ('world', '0021_landslidedeformation_liquefactiondeformation'), ('world', '0022_auto_20150327_1811'), ('world', '0023_auto_20150327_1816'), ('world', '0024_snugget_tsunami_filter'), ('world', '0025_auto_20150328_0041'), ('world', '0026_auto_20150328_0048'), ('world', '0027_auto_20150328_0251'), ('world', '0028_auto_20150328_1835'), ('world', '0029_auto_20150328_1910'), ('world', '0030_auto_20150328_1919'), ('world', '0031_auto_20150328_1930'), ('world', '0032_auto_20150328_2043'), ('world', '0033_auto_20150328_2119'), ('world', '0034_auto_20150328_2120'), ('world', '0035_auto_20150328_2121'), ('world', '0036_auto_20150328_2122'), ('world', '0037_auto_20150328_2124'), ('world', '0038_impactzonedata'), ('world', '0039_auto_20150328_2134'), ('world', '0040_auto_20150328_2150'), ('world', '0041_auto_20150328_2159'), ('world', '0042_auto_20150328_2210'), ('world', '0043_auto_20150328_2242')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TsunamiZone',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('scenario_id', models.IntegerField()),
                ('location', models.CharField(max_length=80)),
                ('scenario_type', models.CharField(max_length=50)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('name', models.CharField(default=None, max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tsunamizone',
            unique_together=set([('scenario_id', 'location')]),
        ),
        migrations.RemoveField(
            model_name='tsunamizone',
            name='name',
        ),
        migrations.CreateModel(
            name='ExpectedGroundShaking',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('rate', models.IntegerField()),
                ('shaking', models.CharField(max_length=11)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImpactZone',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('featureValue', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Infrastructure',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InfrastructureCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InfrastructureGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('items', models.ManyToManyField(to='world.Infrastructure')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecoveryLevels',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('shortLabel', models.CharField(max_length=2)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='infrastructurecategory',
            name='groups',
            field=models.ManyToManyField(to='world.InfrastructureGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='eventOccursRecovery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.RecoveryLevels'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='firstDayRecovery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.RecoveryLevels'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='fourWeeksRecovery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.RecoveryLevels'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='sevenDaysRecovery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.RecoveryLevels'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='sixMonthsRecovery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.RecoveryLevels'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threeDaysRecovery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.RecoveryLevels'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threeMonthsRecovery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.RecoveryLevels'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threePlusYearsRecovery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.RecoveryLevels'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threeYearsRecovery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.RecoveryLevels'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='twelveMonthsRecovery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.RecoveryLevels'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='world.ImpactZone'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructurecategory',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='world.ImpactZone', default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Snugget',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('impact_zone_filter', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SnuggetSection',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SnuggetType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('model_name', models.CharField(choices=[('SNUG_TEXT', 'TextSnugget')], max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextSnugget',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('content', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='snugget',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='world.SnuggetSection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snugget',
            name='shaking_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.ExpectedGroundShaking'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snugget',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='world.SnuggetType'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='snugget',
            name='impact_zone_filter',
        ),
        migrations.AddField(
            model_name='snugget',
            name='temp_text_field',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snugget',
            name='impact_zone_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.ImpactZone'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='LandslideDeformation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('score', models.IntegerField()),
                ('label', models.CharField(max_length=11)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LiquefactionDeformation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('score', models.IntegerField()),
                ('label', models.CharField(max_length=11)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='snugget',
            name='landslide_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.LandslideDeformation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snugget',
            name='liquifaction_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.LiquefactionDeformation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='snugget',
            name='tsunami_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.TsunamiZone'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='SnuggetSubSection',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='snugget',
            name='sub_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, related_name='+', null=True, to='world.SnuggetSubSection'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ImpactZoneData',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('area', models.IntegerField(default=0)),
                ('feature', models.IntegerField(default=0)),
                ('orbndy24', models.IntegerField(default=0)),
                ('orbndy24i', models.IntegerField(default=0)),
                ('perimeter', models.IntegerField(default=0)),
                ('subjstate', models.CharField(default=None, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tsunamizone',
            name='type',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tsunamizone',
            name='typeid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='tsunamizone',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tsunamizone',
            name='scenario_type',
        ),
        migrations.RemoveField(
            model_name='tsunamizone',
            name='scenario_id',
        ),
        migrations.RemoveField(
            model_name='tsunamizone',
            name='location',
        ),
    ]
