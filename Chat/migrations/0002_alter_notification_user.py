# Generated by Django 4.2.2 on 2023-12-22 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0030_alter_userspent_time_created_date'),
        ('Chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.common'),
        ),
    ]
