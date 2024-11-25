# Generated by Django 5.0.7 on 2024-09-05 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_customusermodel_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answermodel',
            name='video',
        ),
        migrations.AddField(
            model_name='videomodel',
            name='answer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.answermodel'),
        ),
    ]
