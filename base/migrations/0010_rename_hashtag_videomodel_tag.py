# Generated by Django 5.0.7 on 2024-08-29 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_videomodel_hashtag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videomodel',
            old_name='hashtag',
            new_name='tag',
        ),
    ]
