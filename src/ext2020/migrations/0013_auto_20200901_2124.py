# Generated by Django 3.0.7 on 2020-09-01 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0027_auto_20200829_1107'),
        ('ext2020', '0012_auto_20200828_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitytrackevent',
            name='begin_time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='begined_communitytrackevent_set', to='events.Time', verbose_name='begin time'),
        ),
        migrations.AddField(
            model_name='communitytrackevent',
            name='end_time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ended_communitytrackevent_set', to='events.Time', verbose_name='end time'),
        ),
    ]
