# Generated by Django 2.1.3 on 2018-11-06 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0005_auto_20181106_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder',
            name='payment_complete',
            field=models.CharField(choices=[('NA', 'No winning bids'), ('N', 'Unpaid'), ('Y', 'Paid')], default='NA', max_length=50),
        ),
    ]
