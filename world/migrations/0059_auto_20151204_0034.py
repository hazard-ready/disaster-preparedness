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
            name='emergency_management_link',
            field=models.URLField(default='http://www.fema.gov', help_text='A link to your local office of emergency management.'),
        ),
        migrations.AddField(
            model_name='location',
            name='evacuation_routes_link',
            field=models.URLField(default='', blank=True, help_text='A link to website that can help people find an evacuation route'),
        ),
    ]
