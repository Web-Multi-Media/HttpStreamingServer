# Generated by Django 2.2.8 on 2020-05-27 11:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('StreamServerApp', '0019_auto_20200527_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservideohistory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uservideohistory',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
