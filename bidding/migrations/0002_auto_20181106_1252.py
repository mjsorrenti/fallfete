# Generated by Django 2.1.3 on 2018-11-06 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bidder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=254)),
                ('mobile_checkout', models.BooleanField()),
                ('payment_complete', models.BooleanField()),
                ('payment_txn', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('bid_amount', models.IntegerField(default=0)),
                ('bidder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bidding.Bidder')),
            ],
        ),
        migrations.DeleteModel(
            name='Bidders',
        ),
    ]
