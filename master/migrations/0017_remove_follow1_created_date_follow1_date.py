# Generated by Django 4.2.2 on 2023-12-01 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0016_remove_follow1_date_follow1_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow1',
            name='created_date',
        ),
        migrations.AddField(
            model_name='follow1',
            name='date',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
