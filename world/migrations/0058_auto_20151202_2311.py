# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0057_auto_20151202_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='about_text',
            field=models.TextField(default='Information about your organization goes here.', help_text='Describe the data and the agencies that it came from.'),
        ),
        migrations.AddField(
            model_name='location',
            name='contact_email',
            field=models.EmailField(default='contact@youremail.com', max_length=254, help_text='Put a contact email for the maintainer of this site here.'),
        ),
    ]
