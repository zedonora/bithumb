# Generated by Django 2.2.3 on 2019-07-14 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0004_bithumb_bitmex_bittrex_coinbase_coinone_korbit_kraken_poloniex_upbit'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.DeleteModel(
            name='Korbit',
        ),
    ]
