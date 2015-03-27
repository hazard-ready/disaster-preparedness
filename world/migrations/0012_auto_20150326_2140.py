# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0011_auto_20150326_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImpactZone',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('featureValue', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Infrastructure',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InfrastructureCategory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InfrastructureGroup',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('items', models.ManyToManyField(to='world.Infrastructure')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecoveryLevels',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('shortLabel', models.CharField(max_length=2)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='infrastructurecategory',
            name='groups',
            field=models.ManyToManyField(to='world.InfrastructureGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='eventOccursRecovery',
            field=models.ForeignKey(related_name='+', to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='firstDayRecovery',
            field=models.ForeignKey(related_name='+', to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='fourWeeksRecovery',
            field=models.ForeignKey(related_name='+', to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='sevenDaysRecovery',
            field=models.ForeignKey(related_name='+', to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='sixMonthsRecovery',
            field=models.ForeignKey(related_name='+', to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threeDaysRecovery',
            field=models.ForeignKey(related_name='+', to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threeMonthsRecovery',
            field=models.ForeignKey(related_name='+', to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threePlusYearsRecovery',
            field=models.ForeignKey(related_name='+', to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='threeYearsRecovery',
            field=models.ForeignKey(related_name='+', to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='twelveMonthsRecovery',
            field=models.ForeignKey(related_name='+', to='world.RecoveryLevels', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='zone',
            field=models.ForeignKey(related_name='+', to='world.ImpactZone', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
    ]
