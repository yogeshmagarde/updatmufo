# Generated by Django 4.2.2 on 2023-12-01 09:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0015_remove_follow_claim_coins_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow1',
            name='date',
        ),
        migrations.AddField(
            model_name='follow1',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
