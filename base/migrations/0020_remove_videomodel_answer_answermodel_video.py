# Generated by Django 5.0.7 on 2024-09-21 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_rename_videourl_videomodel_videourl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videomodel',
            name='answer',
        ),
        migrations.AddField(
            model_name='answermodel',
            name='video',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.videomodel'),
            preserve_default=False,
        ),
    ]
