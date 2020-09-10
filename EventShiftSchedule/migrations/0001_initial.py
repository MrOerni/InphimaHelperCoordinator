# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-19 12:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(blank=True, max_length=64)),
                ('location', models.TextField(blank=True)),
                ('person_in_charge', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('pref_users', models.PositiveIntegerField(default=3)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EventShiftSchedule.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EventShiftSchedule.Position')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginning', models.DateTimeField()),
                ('duration', models.FloatField(blank=True, default=2)),
                ('alt_name', models.CharField(blank=True, max_length=32)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EventShiftSchedule.Event')),
            ],
        ),
        migrations.AddField(
            model_name='slot',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EventShiftSchedule.Time'),
        ),
        migrations.AddField(
            model_name='slot',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='time',
            unique_together=set([('beginning', 'duration', 'event')]),
        ),
        migrations.AlterUniqueTogether(
            name='slot',
            unique_together=set([('time', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='position',
            unique_together=set([('name', 'event')]),
        ),
    ]