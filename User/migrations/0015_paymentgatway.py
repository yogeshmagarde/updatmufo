# Generated by Django 4.2.2 on 2023-10-22 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0014_delete_follow_claim_coins'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paymentgatway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_product', models.CharField(max_length=100)),
                ('order_amount', models.CharField(max_length=25)),
                ('order_payment_id', models.CharField(max_length=100)),
                ('order_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
