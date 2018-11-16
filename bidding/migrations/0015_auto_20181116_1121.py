# Generated by Django 2.1.3 on 2018-11-16 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0014_auto_20181115_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchprocessing',
            name='file',
            field=models.FileField(help_text='Files must be in CSV format. \rItems files should have 2 or 3 columns: id, name, price. \rBidders files should have 4 columns: first_name, last_name, email_address, mobile_checkout (for the last column, any value will be interpretted as True; leave the cell blank for False).', upload_to=''),
        ),
    ]
