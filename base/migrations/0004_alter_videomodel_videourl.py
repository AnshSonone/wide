# Generated by Django 5.0.7 on 2024-08-05 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_customusermodel_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videomodel',
            name='videourl',
            field=models.ImageField(upload_to='video'),
        ),
    ]
