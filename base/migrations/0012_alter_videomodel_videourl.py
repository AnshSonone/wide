# Generated by Django 5.0.7 on 2024-09-02 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_videomodel_tag_answermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videomodel',
            name='videourl',
            field=models.ImageField(blank=True, null=True, upload_to='video'),
        ),
    ]
