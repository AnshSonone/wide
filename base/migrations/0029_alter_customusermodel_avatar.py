# Generated by Django 5.0.7 on 2025-04-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_alter_customusermodel_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='avatar',
            field=models.ImageField(blank=True, default='v1745841895/images_rujcgg.png', upload_to='images/'),
        ),
    ]
