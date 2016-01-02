# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields
import django.db.models.deletion
import django.contrib.gis.db.models.fields

class Migration(migrations.Migration):
    operations = [
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
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('area_name', models.CharField(default='the affected area', help_text="Describe the entire area that this app covers, e.g. 'Oregon' or 'Missoula County'.", max_length=100)),
                ('emergency_management_link', models.URLField(default='http://www.fema.gov', help_text='A link to your local office of emergency management.')),
                ('evacuation_routes_link', models.URLField(default='', help_text='A link to website that can help people find an evacuation route', blank=True)),
                ('disaster_description', models.TextField(help_text='A description of what we are trying to help people prepare for.', default='A natural disaster could strike your area at any time.')),
                ('disaster_name', models.CharField(default='some disaster', help_text="Something like 'a tsunami', 'an earthquake', 'a fire'", max_length=50)),
            ],
            options={
                'verbose_name': 'Location Information'
            },
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
        migrations.CreateModel(
            name='Infrastructure',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('eventOccursRecovery', models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True)),
                ('firstDayRecovery', models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True)),
                ('threeDaysRecovery', models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True)),
                ('sevenDaysRecovery', models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True)),
                ('fourWeeksRecovery', models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True)),
                ('threeMonthsRecovery', models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True)),
                ('sixMonthsRecovery', models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True)),
                ('twelveMonthsRecovery', models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True)),
                ('threeYearsRecovery', models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True)),
                ('threePlusYearsRecovery', models.ForeignKey(to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True)),

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
            name='InfrastructureCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('groups', models.ManyToManyField(to='world.InfrastructureGroup'))
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
            name='SnuggetSection',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SnuggetSubSection',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Snugget',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('section', models.ForeignKey(to='world.SnuggetSection', on_delete=django.db.models.deletion.PROTECT, related_name='+')),
                ('sub_section', models.ForeignKey(to='world.SnuggetSubSection', on_delete=django.db.models.deletion.PROTECT, related_name='+', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TextSnugget',
            fields=[
                ('snugget_ptr', models.OneToOneField(auto_created=True, to='world.Snugget', serialize=False, primary_key=True, parent_link=True)),
                ('content', models.TextField()),
                ('heading', models.TextField(default="")),
                ('image', models.TextField(default="")),
                ('percentage', models.FloatField(null=True)),
            ],
            bases=('world.snugget',),
        ),
        migrations.CreateModel(
            name='EmbedSnugget',
            fields=[
                ('snugget_ptr', models.OneToOneField(auto_created=True, to='world.Snugget', serialize=False, primary_key=True, parent_link=True)),
                ('embed', embed_video.fields.EmbedVideoField()),
            ],
            bases=('world.snugget',),
        ),
    ]
