# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-21 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_attendanceprofile_deleted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendanceprofile',
            name='arrival_date',
            field=models.CharField(blank=True, choices=[('early', 'Early Arrival (Wed-Sat)'), ('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday')], max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='attendanceprofile',
            name='departure_date',
            field=models.DateField(blank=True, choices=[('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday (Man Burn)'), ('sunday', 'Sunday (Temple Burn)'), ('monday', 'Monday (Late Crew)'), ('tuesday', 'Tuesday (Late Crew)')], max_length=16, null=True),
        ),
    ]
