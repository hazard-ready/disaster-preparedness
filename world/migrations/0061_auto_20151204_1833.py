# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0060_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('about_text', models.TextField(default='Information about your organization goes here.', help_text='Describe the data and the agencies that it came from.')),
                ('contact_email', models.EmailField(max_length=254, default='contact@youremail.com', help_text='Put a contact email for the maintainer of this site here.')),
                ('site_url', models.URLField(default='http://www.example.com', help_text='Put the URL to this site here.')),
                ('site_title', models.CharField(max_length=50, default='Your Title Here!')),
                ('site_description', models.CharField(max_length=200, default='A disaster preparedness website', help_text='A small, catchy description for this site.')),
            ],
            options={
                'verbose_name': 'Site Settings',
            },
        ),
        migrations.RemoveField(
            model_name='location',
            name='about_text',
        ),
        migrations.RemoveField(
            model_name='location',
            name='contact_email',
        ),
        migrations.RemoveField(
            model_name='location',
            name='site_description',
        ),
        migrations.RemoveField(
            model_name='location',
            name='site_title',
        ),
        migrations.RemoveField(
            model_name='location',
            name='site_url',
        ),
    ]
