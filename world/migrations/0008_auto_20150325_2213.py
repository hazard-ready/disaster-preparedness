# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0007_auto_20150324_2138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tsunamizone',
            old_name='pid',
            new_name='scenario_id',
        ),
        migrations.RenameField(
            model_name='tsunamizone',
            old_name='type',
            new_name='scenario_type',
        ),
        migrations.AlterUniqueTogether(
            name='tsunamizone',
            unique_together=set([('scenario_id', 'location')]),
        ),
        migrations.RemoveField(
            model_name='tsunamizone',
            name='name',
        ),
    ]
