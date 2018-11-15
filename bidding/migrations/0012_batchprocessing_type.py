# Generated by Django 2.1.3 on 2018-11-15 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0011_batchprocessing'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchprocessing',
            name='type',
            field=models.CharField(choices=[('I', 'Items'), ('B', 'Bidders')], default='Items', max_length=10),
            preserve_default=False,
        ),
    ]