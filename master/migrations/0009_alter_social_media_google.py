# Generated by Django 4.2.2 on 2023-09-20 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0008_alter_social_media_facebook_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='social_media',
            name='Google',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
