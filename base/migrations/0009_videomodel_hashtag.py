# Generated by Django 5.0.7 on 2024-08-29 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_videomodel_videotitle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='videomodel',
            name='hashtag',
            field=models.CharField(default='other', max_length=500),
        ),
    ]