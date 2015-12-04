# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0058_auto_20151202_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='disaster_description',
            field=models.TextField(default='A natural disaster could strike your area at any time.', help_text='A description of what we are trying to help people prepare for.'),
        ),
        migrations.AddField(
            model_name='location',
            name='disaster_name',
            field=models.CharField(default='some disaster', max_length=50, help_text="Something like 'a tsunami', 'an earthquake', 'a fire'"),
        ),
        migrations.AddField(
            model_name='location',
            name='site_description',
            field=models.CharField(default='A disaster preparedness website', max_length=200, help_text='A small, catchy description for this site.'),
        ),
        migrations.AddField(
            model_name='location',
            name='site_title',
            field=models.CharField(default='Your Title Here!', max_length=50),
        ),
        migrations.AddField(
            model_name='location',
            name='site_url',
            field=models.URLField(default='http://www.example.com', help_text='Put the URL to this site here.'),
        ),
    ]
