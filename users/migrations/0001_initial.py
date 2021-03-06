# Generated by Django 3.0.3 on 2020-03-12 16:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField(default=datetime.datetime(2020, 3, 12, 16, 17, 18, 950967, tzinfo=utc))),
                ('rating', models.CharField(max_length=255)),
                ('hold', models.BooleanField(default=False)),
                ('hold_a', models.FloatField(default=0)),
                ('hold_t', models.FloatField(default=0)),
                ('hold_v', models.FloatField()),
                ('trip', models.BooleanField(default=False)),
                ('trip_a', models.FloatField(default=0)),
                ('trip_t', models.FloatField(default=0)),
                ('trip_v', models.FloatField()),
                ('arc', models.BooleanField(default=False)),
                ('cont', models.BooleanField(default=False)),
                ('knr', models.BooleanField(default=False)),
                ('hv', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
