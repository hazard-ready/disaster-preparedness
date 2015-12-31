# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def moveTempTextToTextSnugs(apps, schema_editor):
    Snugget = apps.get_model('world', 'Snugget');
    TextSnugget = apps.get_model('world', 'TextSnugget')
    
    for snugget in Snugget.objects.all():
        textSnug, wasCreated = TextSnugget.objects.get_or_create(snugget_ptr = snugget)
        textSnug.content = snugget.temp_text_field
        textSnug.save()
        

    


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0046_auto_20150417_2234'),
    ]

    operations = [
                  migrations.RunPython(moveTempTextToTextSnugs),
    ]
