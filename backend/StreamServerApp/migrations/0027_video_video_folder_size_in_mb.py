# Generated by Django 4.2 on 2024-08-30 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StreamServerApp', '0026_auto_20240618_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_folder_size_in_MB',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, default=None, null=True),
        ),
    ]
