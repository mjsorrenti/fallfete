# Generated by Django 2.1.3 on 2018-11-06 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0008_auto_20181106_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder',
            name='payment_complete',
            field=models.BooleanField(),
        ),
    ]
