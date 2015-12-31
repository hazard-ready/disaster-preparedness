# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields
import django.db.models.deletion
import django.contrib.gis.db.models.fields

class Migration(migrations.Migration):
    operations = [
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
        migrations.AddField(
            model_name='textsnugget',
            name='snugget_ptr',
            field=models.ForeignKey(to='world.Snugget', db_column='snugget_ptr', null=True),
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
