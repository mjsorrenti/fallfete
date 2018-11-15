# Generated by Django 2.1.3 on 2018-11-15 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0012_batchprocessing_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchprocessing',
            name='file',
            field=models.FileField(help_text='Files must be in CSV format. \nItems files should have 2 columns: id, name \nBidders files should have 4 columns: first_name, last_name, email_address, mobile_checkout (for the last column, any value will be interpretted as True; leave the cell blank for False)', upload_to=''),
        ),
    ]
