# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0048_auto_20150417_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmbedSnugget',
            fields=[
                ('snugget_ptr', models.OneToOneField(serialize=False, to='world.Snugget', primary_key=True, auto_created=True, parent_link=True)),
                ('embed', embed_video.fields.EmbedVideoField()),
            ],
            options={
            },
            bases=('world.snugget',),
        ),
    ]
