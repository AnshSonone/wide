# Generated by Django 5.0.7 on 2025-04-28 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_alter_customusermodel_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='avatar',
            field=models.ImageField(blank=True, default='https://res.cloudinary.com/da25rozpm/image/upload/v1745331876/images_cpca3c.png', upload_to='images/'),
        ),
    ]
