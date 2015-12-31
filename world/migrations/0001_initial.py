# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields
import django.db.models.deletion
import django.contrib.gis.db.models.fields


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# world.migrations.0047_auto_20150417_2236

class Migration(migrations.Migration):

    replaces = [('world', '0001_initial'), ('world', '0002_tsunamizone'), ('world', '0003_tsunamizone_name'), ('world', '0004_auto_20150324_2027'), ('world', '0005_auto_20150324_2057'), ('world', '0006_auto_20150324_2109'), ('world', '0007_auto_20150324_2138'), ('world', '0008_auto_20150325_2213'), ('world', '0009_delete_worldborder'), ('world', '0010_expectedgroundshaking'), ('world', '0011_auto_20150326_2139'), ('world', '0012_auto_20150326_2140'), ('world', '0013_auto_20150326_2151'), ('world', '0014_auto_20150326_2153'), ('world', '0015_infrastructurecategory_zone'), ('world', '0016_auto_20150327_0231'), ('world', '0017_auto_20150327_0255'), ('world', '0018_snugget_impact_zone_filter'), ('world', '0019_auto_20150327_0259'), ('world', '0020_auto_20150327_0300'), ('world', '0021_landslidedeformation_liquefactiondeformation'), ('world', '0022_auto_20150327_1811'), ('world', '0023_auto_20150327_1816'), ('world', '0024_snugget_tsunami_filter'), ('world', '0025_auto_20150328_0041'), ('world', '0026_auto_20150328_0048'), ('world', '0027_auto_20150328_0251'), ('world', '0028_auto_20150328_1835'), ('world', '0029_auto_20150328_1910'), ('world', '0030_auto_20150328_1919'), ('world', '0031_auto_20150328_1930'), ('world', '0032_auto_20150328_2043'), ('world', '0033_auto_20150328_2119'), ('world', '0034_auto_20150328_2120'), ('world', '0035_auto_20150328_2121'), ('world', '0036_auto_20150328_2122'), ('world', '0037_auto_20150328_2124'), ('world', '0038_impactzonedata'), ('world', '0039_auto_20150328_2134'), ('world', '0040_auto_20150328_2150'), ('world', '0041_auto_20150328_2159'), ('world', '0042_auto_20150328_2210'), ('world', '0043_auto_20150328_2242'), ('world', '0044_auto_20150328_2316'), ('world', '0045_textsnugget_snugget_ptr'), ('world', '0046_auto_20150417_2234'), ('world', '0047_auto_20150417_2236'), ('world', '0048_auto_20150417_2254'), ('world', '0049_embedsnugget'), ('world', '0050_auto_20150430_2046'), ('world', '0051_auto_20150430_2053'), ('world', '0052_auto_20150625_1913'), ('world', '0053_tsunamizone'), ('world', '0054_auto_20151202_0307'), ('world', '0055_auto_20151202_2007'), ('world', '0056_auto_20151202_2027'), ('world', '0057_auto_20151202_2046'), ('world', '0058_auto_20151202_2311'), ('world', '0059_auto_20151204_0034'), ('world', '0059_auto_20151202_2347'), ('world', '0060_merge'), ('world', '0061_auto_20151204_1833')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TsunamiZone',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('scenario_id', models.IntegerField()),
                ('location', models.CharField(max_length=80)),
                ('scenario_type', models.CharField(max_length=50)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('name', models.CharField(default=None, max_length=80)),
            ],
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('rate', models.IntegerField()),
                ('shaking', models.CharField(max_length=11)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992)),
            ],
        ),
        migrations.CreateModel(
            name='ImpactZone',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('featureValue', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Infrastructure',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='InfrastructureCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='InfrastructureGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('items', models.ManyToManyField(to='world.Infrastructure')),
            ],
        ),
        migrations.CreateModel(
            name='RecoveryLevels',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('shortLabel', models.CharField(max_length=2)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='infrastructurecategory',
            name='groups',
            field=models.ManyToManyField(to='world.InfrastructureGroup'),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='eventOccursRecovery',
            field=models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='firstDayRecovery',
            field=models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='fourWeeksRecovery',
            field=models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='sevenDaysRecovery',
            field=models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='sixMonthsRecovery',
            field=models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threeDaysRecovery',
            field=models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threeMonthsRecovery',
            field=models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threePlusYearsRecovery',
            field=models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threeYearsRecovery',
            field=models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='twelveMonthsRecovery',
            field=models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='zone',
            field=models.ForeignKey(to='world.ImpactZone', on_delete=django.db.models.deletion.PROTECT, related_name='+'),
        ),
        migrations.AddField(
            model_name='infrastructurecategory',
            name='zone',
            field=models.ForeignKey(to='world.ImpactZone', on_delete=django.db.models.deletion.PROTECT, related_name='+', default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Snugget',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('impact_zone_filter', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SnuggetSection',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SnuggetType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('model_name', models.CharField(choices=[('SNUG_TEXT', 'TextSnugget')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TextSnugget',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('content', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='snugget',
            name='section',
            field=models.ForeignKey(to='world.SnuggetSection', on_delete=django.db.models.deletion.PROTECT, related_name='+'),
        ),
        migrations.AddField(
            model_name='snugget',
            name='shaking_filter',
            field=models.ForeignKey(to='world.ExpectedGroundShaking', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='snugget',
            name='type',
            field=models.ForeignKey(to='world.SnuggetType', on_delete=django.db.models.deletion.PROTECT, related_name='+'),
        ),
        migrations.RemoveField(
            model_name='snugget',
            name='impact_zone_filter',
        ),
        migrations.AddField(
            model_name='snugget',
            name='temp_text_field',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='snugget',
            name='impact_zone_filter',
            field=models.ForeignKey(to='world.ImpactZone', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.CreateModel(
            name='LandslideDeformation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('score', models.IntegerField()),
                ('label', models.CharField(max_length=11)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992)),
            ],
        ),
        migrations.CreateModel(
            name='LiquefactionDeformation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('score', models.IntegerField()),
                ('label', models.CharField(max_length=11)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=2992)),
            ],
        ),
        migrations.AddField(
            model_name='snugget',
            name='landslide_filter',
            field=models.ForeignKey(to='world.LandslideDeformation', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='snugget',
            name='liquifaction_filter',
            field=models.ForeignKey(to='world.LiquefactionDeformation', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='snugget',
            name='tsunami_filter',
            field=models.ForeignKey(to='world.TsunamiZone', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.CreateModel(
            name='SnuggetSubSection',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='snugget',
            name='sub_section',
            field=models.ForeignKey(to='world.SnuggetSubSection', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ImpactZoneData',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('shape_area', models.FloatField(default=1)),
                ('shape_leng', models.FloatField(default=1)),
                ('zone', models.CharField(default=1, max_length=10)),
                ('zoneid', models.IntegerField(default=1)),
            ],
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
        migrations.AddField(
            model_name='textsnugget',
            name='snugget_ptr',
            field=models.ForeignKey(to='world.Snugget', db_column='snugget_ptr', null=True),
        ),
        migrations.RunPython(
            code=world.migrations.0047_auto_20150417_2236.moveTempTextToTextSnugs,
        ),
        migrations.RemoveField(
            model_name='textsnugget',
            name='id',
        ),
        migrations.AlterField(
            model_name='textsnugget',
            name='snugget_ptr',
            field=models.OneToOneField(auto_created=True, to='world.Snugget', serialize=False, primary_key=True, parent_link=True),
        ),
        migrations.CreateModel(
            name='EmbedSnugget',
            fields=[
                ('snugget_ptr', models.OneToOneField(auto_created=True, to='world.Snugget', serialize=False, primary_key=True, parent_link=True)),
                ('embed', embed_video.fields.EmbedVideoField()),
            ],
            bases=('world.snugget',),
        ),
        migrations.RemoveField(
            model_name='snugget',
            name='type',
        ),
        migrations.AlterField(
            model_name='snugget',
            name='temp_text_field',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='snugget',
            name='temp_text_field',
            field=models.TextField(editable=False, null=True, blank=True),
        ),
        migrations.RemoveField(
            model_name='snugget',
            name='tsunami_filter',
        ),
        migrations.DeleteModel(
            name='TsunamiZone',
        ),
        migrations.CreateModel(
            name='TsunamiZone',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('typeid', models.IntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('area_name', models.CharField(default='the affected area', help_text="Describe the entire area that this app covers, e.g. 'Oregon' or 'Missoula County'.", max_length=100)),
            ],
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Location Information'},
        ),
        migrations.AlterField(
            model_name='location',
            name='area_name',
            field=models.CharField(default='the affected area', help_text="Describe the entire area that this app covers, e.g. 'Oregon' or 'Missoula County'.", max_length=100),
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='shape_area',
        ),
        migrations.RemoveField(
            model_name='impactzonedata',
            name='shape_leng',
        ),
        migrations.AddField(
            model_name='location',
            name='emergency_management_link',
            field=models.URLField(default='http://www.fema.gov', help_text='A link to your local office of emergency management.'),
        ),
        migrations.AddField(
            model_name='location',
            name='evacuation_routes_link',
            field=models.URLField(default='', help_text='A link to website that can help people find an evacuation route', blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='disaster_description',
            field=models.TextField(help_text='A description of what we are trying to help people prepare for.', default='A natural disaster could strike your area at any time.'),
        ),
        migrations.AddField(
            model_name='location',
            name='disaster_name',
            field=models.CharField(default='some disaster', help_text="Something like 'a tsunami', 'an earthquake', 'a fire'", max_length=50),
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('about_text', models.TextField(help_text='Describe the data and the agencies that it came from.', default='Information about your organization goes here.')),
                ('contact_email', models.EmailField(default='contact@youremail.com', help_text='Put a contact email for the maintainer of this site here.', max_length=254)),
                ('site_url', models.URLField(default='http://www.example.com', help_text='Put the URL to this site here.')),
                ('site_title', models.CharField(default='Your Title Here!', max_length=50)),
                ('site_description', models.CharField(default='A disaster preparedness website', help_text='A small, catchy description for this site.', max_length=200)),
            ],
            options={
                'verbose_name': 'Site Settings',
            },
        ),
    ]
